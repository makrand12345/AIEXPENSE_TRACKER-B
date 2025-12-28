import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Header
from bson import ObjectId
from app.config.database import get_user_collection

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY not set. Configure it in Vercel project settings."
        )
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(authorization: str = Header(None)):
    if not SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="SECRET_KEY not configured. Set it in Vercel project settings."
        )
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_collection = get_user_collection()
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {"id": user["_id"], "email": user["email"]}
