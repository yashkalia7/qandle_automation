from fastapi import FastAPI
from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from notifications import send_daily_notifications
from router import router
import os

# Load from .env file first, then override with actual environment variables.
# Locally: reads .env file. On Render: .env file doesn't exist, so os.environ takes over.
config = {**dotenv_values(".env"), **os.environ}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to MongoDB + start cron
    app.mongodb_client = AsyncIOMotorClient(config["MONGO_URI"])
    app.db = app.mongodb_client[config.get("DB_NAME", "qandle")]
    print("Connected to MongoDB")

    # Start the scheduler — sends notifications daily at 12 PM
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_notifications, "cron", hour=12, minute=0, args=[app])
    scheduler.start()

    yield

    # Shutdown: close MongoDB + stop cron
    scheduler.shutdown()
    app.mongodb_client.close()
    print("Disconnected from MongoDB")


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Qandle Attendance Backend"}
