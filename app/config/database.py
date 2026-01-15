import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings

MONGO_URI = settings.MONGO_URI
print(f"Initializing database configuration...{settings.MONGO_URI}")

print(f"Database config - MONGO_URI set: {MONGO_URI is not None} MONGO_URI: {MONGO_URI}")

# Lazy initialization - don't connect until first use
_client = None
_db = None
_user_collection = None
_expense_collection = None
_initialized = False

def get_user_collection():
    """Get user collection, initializing DB if needed"""
    global _client, _db, _user_collection, _initialized
    
    if _initialized:
        return _user_collection
    
    if not MONGO_URI:
        raise RuntimeError(
            "MONGO_URI not set. Configure it in Vercel project settings."
        )
    
    try:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        _client.admin.command('ping')
        _db = _client["ai_expense_tracker"]
        _user_collection = _db["users"]
        _initialized = True
        return _user_collection
    except ServerSelectionTimeoutError as e:
        raise RuntimeError(
            f"Cannot connect to MongoDB. Check MONGO_URI and MongoDB Atlas network access."
        ) from e

def get_expense_collection():
    """Get expense collection, initializing DB if needed"""
    global _client, _db, _expense_collection, _initialized
    
    if _initialized:
        return _expense_collection
    
    if not MONGO_URI:
        raise RuntimeError(
            "MONGO_URI not set. Configure it in Vercel project settings."
        )
    
    try:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        _client.admin.command('ping')
        _db = _client["ai_expense_tracker"]
        _expense_collection = _db["expenses"]
        _initialized = True
        return _expense_collection
    except ServerSelectionTimeoutError as e:
        raise RuntimeError(
            f"Cannot connect to MongoDB. Check MONGO_URI and MongoDB Atlas network access."
        ) from e

# Legacy exports for backward compatibility - these are None until first use
user_collection = None
expense_collection = None


