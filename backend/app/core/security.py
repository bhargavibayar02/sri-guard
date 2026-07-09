# security.py
# Handles two things:
# 1. Hashing and checking passwords (so we never store plain-text passwords)
# 2. Creating and verifying JWT tokens (so users stay "logged in")

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings

# This object knows how to hash passwords using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Turns a plain password like 'admin123' into a scrambled hash for safe storage."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Creates a JWT token containing 'data' (usually the username),
    with an expiry time attached, signed with our secret key.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Verifies a JWT token is valid and not expired.
    Returns the decoded data if valid, or None if invalid/expired.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None