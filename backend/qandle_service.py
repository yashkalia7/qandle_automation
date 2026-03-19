import httpx
from datetime import datetime, timedelta, timezone

QANDLE_BASE_URL = "https://hrconnect.qandle.com"
CATEGORY_ID = "5d389c7839473e6a728b92dc"

# IST offset
IST = timezone(timedelta(hours=5, minutes=30))

BROWSER_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": QANDLE_BASE_URL,
    "Referer": f"{QANDLE_BASE_URL}/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "browserName": "Chrome",
    "browserVersion": "143.0.0.0",
    "device": "website",
}


async def qandle_login(emp_code: str, password: str) -> dict:
    """Login to Qandle HRMS and return the response containing the JWT token."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{QANDLE_BASE_URL}/auth/login",
            content=f"password={password}&emp_code={emp_code}",
            headers={
                **BROWSER_HEADERS,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        resp.raise_for_status()
        return resp.json()


def _build_regularize_form(date_str: str, time_in: str, time_out: str, comment: str) -> dict:
    """
    Build the multipart form fields for the regularization request.

    Args:
        date_str: Date to regularize, e.g. "19-Mar-2026"
        time_in: Clock-in time in HH:MM 24h IST, e.g. "09:30"
        time_out: Clock-out time in HH:MM 24h IST, e.g. "21:42"
        comment: Reason/comment for regularization
    """
    # Parse the date
    dt = datetime.strptime(date_str, "%d-%b-%Y")
    date_formatted = dt.strftime("%d-%b-%Y")  # "19-Mar-2026"
    date_timestamp = str(int(dt.replace(tzinfo=IST).timestamp()))

    # Build ISO in_time and out_time (convert IST to UTC)
    in_h, in_m = map(int, time_in.split(":"))
    out_h, out_m = map(int, time_out.split(":"))

    in_dt_ist = dt.replace(hour=in_h, minute=in_m, tzinfo=IST)
    out_dt_ist = dt.replace(hour=out_h, minute=out_m, tzinfo=IST)

    in_time_utc = in_dt_ist.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    out_time_utc = out_dt_ist.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    return {
        "category": CATEGORY_ID,
        "request_data[0][is_clock_out_selfie]": "false",
        "request_data[0][is_clock_in_selfie]": "false",
        "request_data[0][date]": date_formatted,
        "request_data[0][date_formated]": date_formatted,
        "request_data[0][date_timestamp]": date_timestamp,
        "request_data[0][total_break_hours]": "00.00",
        "request_data[0][cal_total_break_hours]": "0",
        "request_data[0][in_time]": in_time_utc,
        "request_data[0][out_time]": out_time_utc,
        "request_data[0][total_hours]": "0",
        "request_data[0][total_hours_seconds]": "00:00:00",
        "request_data[0][cal_total_hours]": "0",
        "request_data[0][total_working_hours]": "0",
        "request_data[0][source]": "",
        "request_data[0][total_break_hours_formatted]": "00:00",
        "request_data[0][is_week_off]": "false",
        "request_data[0][holiday]": "false",
        "request_data[0][is_calender_holiday]": "false",
        "request_data[0][holiday_reason]": "",
        "request_data[0][remark]": "",
        "request_data[0][is_autoclockout]": "false",
        "request_data[0][is_regularised]": "false",
        "request_data[0][flag]": "false",
        "request_data[0][isIndividual]": "true",
        "request_data[0][isCheck]": "false",
        "request_data[0][start_time]": time_in,
        "request_data[0][end_time]": time_out,
        "comment": comment,
        "doc_file": "null",
    }


async def qandle_regularize(token: str, date_str: str, time_in: str, time_out: str, comment: str) -> dict:
    """
    Call the Qandle regularization API.

    Args:
        token: JWT Bearer token from login
        date_str: Date to regularize, e.g. "19-Mar-2026"
        time_in: Clock-in time HH:MM 24h IST
        time_out: Clock-out time HH:MM 24h IST
        comment: Reason for regularization
    """
    form_data = _build_regularize_form(date_str, time_in, time_out, comment)

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{QANDLE_BASE_URL}/timeattendance/employee/regularization",
            data=form_data,
            headers={
                **BROWSER_HEADERS,
                "Authorization": f"Bearer {token}",
            },
        )
        resp.raise_for_status()
        return resp.json()
