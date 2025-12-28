from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_routes import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.expenses import router as expense_router
from app.routes.analytics import router as analytics_router
from app.routes.finance import router as finance_router

app = FastAPI(title="AI Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aiexpense-tracker-f.vercel.app",
        "https://aiexpense-tracker-b.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(expense_router, prefix="/expenses", tags=["Expenses"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(finance_router, prefix="/finance", tags=["Finance"])

@app.get("/")
def root():
    return {"message": "API running"}
