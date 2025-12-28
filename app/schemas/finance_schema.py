from pydantic import BaseModel
from typing import Optional

class FinanceProfileCreate(BaseModel):
    monthly_income: float
    fixed_expenses: float
    investments: float
    liabilities: float
    risk_level: str
    financial_goal: Optional[str] = None
