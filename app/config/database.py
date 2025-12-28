import os
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["ai_expense_tracker"]

user_collection = db["users"]
expense_collection = db["expenses"]
