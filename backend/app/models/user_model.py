# user_model.py
# Defines what a "User" (SOC Analyst) looks like, and what
# data is expected in login requests/responses.

from pydantic import BaseModel

class UserLogin(BaseModel):
    """What the frontend sends when logging in."""
    username: str
    password: str

class UserOut(BaseModel):
    """What we send back to the frontend after successful login."""
    username: str
    role: str

class Token(BaseModel):
    """The JWT token response shape."""
    access_token: str
    token_type: str = "bearer"