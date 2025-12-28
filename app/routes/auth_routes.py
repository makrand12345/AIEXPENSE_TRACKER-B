from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_service import create_user, authenticate_user
from app.core.jwt import create_access_token

router = APIRouter()

@router.post("/signup")
def signup(data: UserCreate):
    user_id = create_user(
        data.name,
        data.email,
        data.password,
        data.profession
    )

    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "Signup successful"}

@router.post("/login")
def login(data: UserLogin):
    user = authenticate_user(data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}
