from fastapi import APIRouter, Request
from models import DeviceRegister, RegularizeRequest, UserRegister
from datetime import datetime, timedelta, timezone
from qandle_service import qandle_login, qandle_regularize

IST = timezone(timedelta(hours=5, minutes=30))

router = APIRouter()


@router.post("/register-device")
async def register_device(device: DeviceRegister, request: Request):
    db = request.app.db

    await db.devices.update_one(
        {"user_id": device.user_id},
        {"$set": {
            "user_name": device.user_name,
            "push_token": device.push_token,
            "platform": device.platform,
            "updated_at": datetime.utcnow(),
            "is_active": True,
        },
        "$setOnInsert": {
            "created_at": datetime.utcnow(),
        }},
        upsert=True
    )

    return {"message": "Device registered successfully"}


@router.post("/register-user")
async def register_user(user: UserRegister, request: Request):
    db = request.app.db

    await db.users.update_one(
        {"emp_code": user.emp_code},
        {"$set": user.model_dump()},
        upsert=True
    )

    return {"message": "User registered successfully"}


@router.get("/user/{user_id}")
async def get_user(user_id: str, request: Request):
    db = request.app.db
    device = await db.devices.find_one({"user_id": user_id}, {"_id": 0})
    if not device:
        return {"error": "User not found"}
    return device


@router.post("/attendance/regularize")
async def regularize(body: RegularizeRequest, request: Request):
    db = request.app.db

    user = await db.users.find_one({"emp_code": body.user_id})
    if not user:
        return {"error": "User not found"}

    # Step 1: Login to Qandle to get JWT token
    try:
        login_resp = await qandle_login(user["emp_code"], user["password"])
    except Exception as e:
        await db.regularization_logs.insert_one({
            "user_id": body.user_id,
            "status": "login_failed",
            "error": str(e),
            "timestamp": datetime.utcnow(),
        })
        return {"error": f"Qandle login failed: {str(e)}"}

    token = login_resp.get("data", {}).get("accessToken")
    if not token:
        await db.regularization_logs.insert_one({
            "user_id": body.user_id,
            "status": "login_failed",
            "error": "No accessToken in login response",
            "response": str(login_resp),
            "timestamp": datetime.utcnow(),
        })
        return {"error": "Could not extract token from Qandle login", "login_response": login_resp}

    # Step 2: Determine date (default: today IST)
    date_str = body.date
    if not date_str:
        today_ist = datetime.now(IST)
        date_str = today_ist.strftime("%d-%b-%Y")

    # Step 3: Call Qandle regularization API
    comment = body.comment or "office"
    try:
        reg_resp = await qandle_regularize(
            token=token,
            date_str=date_str,
            time_in=user["time_in"],
            time_out=user["time_out"],
            comment=comment,
        )
    except Exception as e:
        await db.regularization_logs.insert_one({
            "user_id": body.user_id,
            "status": "regularize_failed",
            "error": str(e),
            "date": date_str,
            "timestamp": datetime.utcnow(),
        })
        return {"error": f"Qandle regularization failed: {str(e)}"}

    # Step 4: Log success
    await db.regularization_logs.insert_one({
        "user_id": body.user_id,
        "status": "success",
        "date": date_str,
        "qandle_response": str(reg_resp),
        "timestamp": datetime.utcnow(),
    })

    return {
        "message": f"Regularization submitted for {body.user_id} on {date_str}",
        "qandle_response": reg_resp,
    }
