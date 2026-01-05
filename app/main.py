from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

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
        "https://aiexpense-tracker-b.onrender.com",
        "http://localhost:3000",
        "http://localhost:5173"
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
    """Root endpoint - check if API is configured"""
    missing_vars = []
    if not os.getenv("MONGO_URI"):
        missing_vars.append("MONGO_URI")
    if not os.getenv("SECRET_KEY"):
        missing_vars.append("SECRET_KEY")
    
    if missing_vars:
        return {
            "message": "⚠️ API is running but not fully configured",
            "status": "incomplete",
            "missing_env_vars": missing_vars,
            "instructions": "Set these environment variables in Vercel project settings"
        }
    
    return {"message": "API running", "status": "configured"}

@app.get("/health")
def health_check():
    """Health check endpoint - no authentication required"""
    return {"status": "healthy", "service": "AI Expense Tracker API"}

