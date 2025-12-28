from fastapi import APIRouter, Depends, HTTPException
from app.core.jwt import get_current_user
from app.config.database import user_collection
from app.schemas.finance_schema import FinanceProfileCreate

router = APIRouter()

@router.get("/me")
def get_finance_profile(current_user: dict = Depends(get_current_user)):
    user = user_collection.find_one({"_id": current_user["id"]})
    if not user or "finance_profile" not in user:
        raise HTTPException(status_code=404, detail="Finance profile not set")
    return user["finance_profile"]

@router.post("/me")
def save_finance_profile(
    data: FinanceProfileCreate,
    current_user: dict = Depends(get_current_user)
):
    user_collection.update_one(
        {"_id": current_user["id"]},
        {"$set": {"finance_profile": data.dict()}}
    )
    return {"message": "Finance profile saved"}
