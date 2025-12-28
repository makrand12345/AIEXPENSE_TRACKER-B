from fastapi import APIRouter, Depends
from datetime import datetime
from app.core.jwt import get_current_user
from app.config.database import expense_collection, user_collection

router = APIRouter()

@router.get("/overview")
def analytics_overview(current_user: dict = Depends(get_current_user)):
    user = user_collection.find_one({"_id": current_user["id"]})
    finance = user.get("finance_profile")

    if not finance:
        return {"warning": "Finance profile not completed"}

    expenses = list(expense_collection.find({
        "user_id": current_user["id"]
    }))

    total_spent = sum(e["amount"] for e in expenses)

    disposable_income = (
        finance["monthly_income"]
        - finance["fixed_expenses"]
        - finance["liabilities"]
    )

    insight = (
        "You are overspending relative to your income"
        if total_spent > disposable_income
        else "Your spending is within healthy limits"
    )

    return {
        "total_spent": total_spent,
        "disposable_income": disposable_income,
        "investment_ratio": round(
            finance["investments"] / finance["monthly_income"], 2
        ),
        "risk_level": finance["risk_level"],
        "insight": insight,
    }
