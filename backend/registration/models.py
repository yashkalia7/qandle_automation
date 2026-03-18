#this is the models.py file for writing how the model of each class look like
from typing import Optional

from pydantic import BaseModel
class User(BaseModel):
    name: str
    qandle_email:str
    qandle_emp_code:str
    password:str
    #what will be asking from the frontend focused acc
    notification_time_of_the_day:str
    reason:str
    time_in:str
    time_out:Optional[str]#always time in + 9h



