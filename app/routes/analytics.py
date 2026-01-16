from fastapi import APIRouter, Depends
from app.core.jwt import get_current_user
from app.config.database import get_user_collection, get_expense_collection

router = APIRouter()  # ✅ THIS LINE WAS MISSING


@router.get("/overview")
def analytics_overview(current_user: dict = Depends(get_current_user)):
    user_collection = get_user_collection()
    expense_collection = get_expense_collection()

    user = user_collection.find_one({"_id": current_user["id"]})

    if not user or "finance_profile" not in user:
        return {
            "total_spent": 0,
            "disposable_income": 0,
            "investment_ratio": 0,
            "risk_level": None,
            "insight": "Complete your finance profile to see insights"
        }

    finance = user["finance_profile"]

    expenses = list(
        expense_collection.find({"user_id": current_user["id"]})
    )

    total_spent = sum(e.get("amount", 0) for e in expenses)

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
