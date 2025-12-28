from fastapi import APIRouter, Depends
from bson import ObjectId
from datetime import datetime

from app.config.database import expense_collection
from app.schemas.expense_schema import ExpenseCreate
from app.models.expense_model import expense_helper
from app.core.jwt import get_current_user

router = APIRouter()

# 📥 Get expenses (USER-SPECIFIC)
@router.get("/")
def get_expenses(current_user: dict = Depends(get_current_user)):
    expenses = []

    cursor = expense_collection.find(
        {"user_id": current_user["id"]}
    ).sort("created_at", -1)

    for expense in cursor:
        expenses.append(expense_helper(expense))

    return expenses


# ➕ Add expense (AUTO user_id + timestamp)
@router.post("/")
def add_expense(
    expense: ExpenseCreate,
    current_user: dict = Depends(get_current_user)
):
    expense_data = {
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "color": expense.color,
        "user_id": current_user["id"],
        "created_at": datetime.utcnow(),
    }

    result = expense_collection.insert_one(expense_data)
    new_expense = expense_collection.find_one(
        {"_id": result.inserted_id}
    )

    return expense_helper(new_expense)


# ❌ Delete expense (OWNER ONLY)
@router.delete("/{expense_id}")
def delete_expense(
    expense_id: str,
    current_user: dict = Depends(get_current_user)
):
    expense_collection.delete_one({
        "_id": ObjectId(expense_id),
        "user_id": current_user["id"],
    })

    return {"message": "Expense deleted"}
