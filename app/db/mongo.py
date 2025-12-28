from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable not set")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client["ai_expense_tracker"]
    users_collection = db["users"]
    expenses_collection = db["expenses"]
except ServerSelectionTimeoutError:
    raise RuntimeError(f"Could not connect to MongoDB at {MONGO_URI}")
