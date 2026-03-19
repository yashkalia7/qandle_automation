from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Request: when app registers a device
class DeviceRegister(BaseModel):
    user_id: str
    user_name: str
    push_token: str
    platform: str  # "android" or "ios"


# What gets stored in MongoDB devices collection
class DeviceInDB(BaseModel):
    user_id: str
    user_name: str
    push_token: str
    platform: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


# Request: when user taps "Yes" on notification
class RegularizeRequest(BaseModel):
    user_id: str  # emp_code of the user
    date: Optional[str] = None  # e.g. "19-Mar-2026", defaults to today
    comment: Optional[str] = "office"  # reason for regularization


# Request: user registration with Qandle credentials
class UserRegister(BaseModel):
    name: str
    email: str
    time_in: str
    time_out: str
    emp_code: str
    password: str
