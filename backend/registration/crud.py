#here we need to write fastapi endpoints for 
#in order to perform crud operations on the user models
from fastapi import FastAPI
from contextlib import asynccontextmanager
from models import User
from database import create_mongo_client, get_database
from fastapi import Request
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    mongo_client = create_mongo_client()
    db = get_database(mongo_client)

    app.mongodb_client = mongo_client
    app.database = db

    print("Connected to MongoDB")
    yield

    # 🔹 Shutdown
    mongo_client.close()
    print("Disconnected from MongoDB")

app = FastAPI(lifespan=lifespan)

#we will be using lifespan instead of simply calling the db here!
#adding a user to the table
@app.post("/register")
async def reg_user(request:Request,input:User):
    print(f"testing if actually came in {input}")
    db=request.app.database
    db["users"].insert_one(input.model_dump())
    return {"ok":True}
    