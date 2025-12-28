def expense_helper(expense) -> dict:
    return {
        "id": str(expense["_id"]),
        "title": expense["title"],
        "amount": expense["amount"],
        "category": expense.get("category", "general"),
        "color": expense.get("color", "#4F46E5"),
        "created_at": expense["created_at"],
    }
