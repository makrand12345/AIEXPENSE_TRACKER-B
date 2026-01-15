from fastapi import APIRouter, Depends
from app.core.jwt import get_current_user
from app.config.database import get_user_collection
from app.schemas.finance_schema import FinanceProfileCreate
from bson import ObjectId

router = APIRouter()

@router.get("/me")
def get_finance_profile(current_user: dict = Depends(get_current_user)):
    user_collection = get_user_collection()

    user = user_collection.find_one({"_id": ObjectId(current_user["id"])})

    if not user:
        return {
            "has_profile": False,
            "finance_profile": None
        }

    finance_profile = user.get("finance_profile")

    return {
        "has_profile": finance_profile is not None,
        "finance_profile": finance_profile
    }


@router.post("/me")
def save_finance_profile(
    data: FinanceProfileCreate,
    current_user: dict = Depends(get_current_user)
):
    user_collection = get_user_collection()

    user_collection.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$set": {"finance_profile": data.dict()}}
    )

    return {"message": "Finance profile saved"}
