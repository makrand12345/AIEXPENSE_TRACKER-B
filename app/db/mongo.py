from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Initialize as None; will be connected on first request if env var is set
client = None
db = None
users_collection = None
expenses_collection = None

def _init_db():
    """Initialize database connection on first use"""
    global client, db, users_collection, expenses_collection
    
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
        users_collection = db["users"]
        expenses_collection = db["expenses"]
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

