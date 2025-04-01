from fastapi import APIRouter, Request, HTTPException
from app.agents.postgres import PostgresAgent
from app.config import settings
from app.models.user import UserCreate, UserPublic
from app.core.security import create_access_token
from datetime import timedelta
from typing import Any
from app.api.deps import CurrentUser

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/register")
async def register_user(request: Request, user: UserCreate):
    return await PostgresAgent().create_user(user)

@user_router.post("/login")
async def login_user(request: Request, user: UserCreate):
    user: UserPublic = await PostgresAgent().login_user(user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@user_router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user

