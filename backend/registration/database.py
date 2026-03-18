# print(pymongo.__version__)
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def create_mongo_client():
    return MongoClient(os.getenv("mongo_string"))

def get_database(client: MongoClient):
    return client["qandle"]
