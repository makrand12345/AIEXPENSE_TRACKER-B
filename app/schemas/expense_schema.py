from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: Optional[str] = "general"
    color: Optional[str] = "#4F46E5"  # default indigo

class ExpenseResponse(BaseModel):
    id: str
    title: str
    amount: float
    category: str
    color: str
    created_at: datetime
