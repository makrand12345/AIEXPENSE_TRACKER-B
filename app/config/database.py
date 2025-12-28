import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable not set")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client["ai_expense_tracker"]
    user_collection = db["users"]
    expense_collection = db["expenses"]
except ServerSelectionTimeoutError:
    raise RuntimeError(f"Could not connect to MongoDB at {MONGO_URI}")
