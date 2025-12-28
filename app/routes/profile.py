from fastapi import APIRouter, Depends, HTTPException
from app.config.database import get_user_collection
from app.core.jwt import get_current_user
from pydantic import BaseModel

router = APIRouter()

class ProfileUpdate(BaseModel):
    name: str | None = None
    avatar: str | None = None


@router.get("/me")
def get_profile(current_user: dict = Depends(get_current_user)):
    user_collection = get_user_collection()
    user = user_collection.find_one({"_id": current_user["id"]})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name", ""),
        "avatar": user.get("avatar", ""),
        "finance_profile": user.get("finance_profile")
    }


@router.put("/me")
def update_profile(
    data: ProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    user_collection = get_user_collection()
    user_collection.update_one(
        {"_id": current_user["id"]},
        {"$set": data.dict(exclude_none=True)}
    )

    return {"message": "Profile updated"}
