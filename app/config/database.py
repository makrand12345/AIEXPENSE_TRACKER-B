from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings

MONGO_URI = settings.MONGO_URI

_client = None
_db = None


def _init_db():
    global _client, _db

    if _db is not None:
        return

    if not MONGO_URI:
        raise RuntimeError("MONGO_URI not set")

    try:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
        _db = _client["ai_expense_tracker"]
    except ServerSelectionTimeoutError as e:
        raise RuntimeError("Cannot connect to MongoDB") from e


def get_user_collection():
    _init_db()
    return _db["users"]


def get_expense_collection():
    _init_db()
    return _db["expenses"]
