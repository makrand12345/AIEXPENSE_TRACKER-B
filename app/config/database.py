import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = os.getenv("MONGO_URI")

# Initialize as None; will be connected on first request if env var is set
client = None
db = None
user_collection = None
expense_collection = None

def _init_db():
    """Initialize database connection on first use"""
    global client, db, user_collection, expense_collection
    
    if client is not None:
        return  # Already initialized
    
    if not MONGO_URI:
        raise RuntimeError(
            "MONGO_URI environment variable not set. "
            "Set it in Vercel project settings or .env file"
        )
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client["ai_expense_tracker"]
        user_collection = db["users"]
        expense_collection = db["expenses"]
    except ServerSelectionTimeoutError as e:
        raise RuntimeError(
            f"Could not connect to MongoDB at {MONGO_URI}. "
            f"Check your connection string and MongoDB Atlas network access rules."
        ) from e

# Call on import to validate early, but don't fail if env var not set yet
try:
    _init_db()
except RuntimeError:
    # Allow app to start; will fail with clear error on first API call
    pass

