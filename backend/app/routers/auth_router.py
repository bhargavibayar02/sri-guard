# auth_router.py
# Exposes the /auth/login endpoint.

from fastapi import APIRouter, HTTPException
from app.models.user_model import UserLogin
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(credentials: UserLogin):
    """
    SOC Analyst login endpoint.
    Takes username + password, returns a JWT token if valid.
    """
    result = await authenticate_user(credentials.username, credentials.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return result