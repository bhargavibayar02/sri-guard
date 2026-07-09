# auth_service.py
# Contains the actual logic for checking login credentials.

from app.database.mongodb import users_collection
from app.core.security import verify_password, create_access_token


async def authenticate_user(username: str, password: str):
    """
    Looks up the user in MongoDB, checks the password,
    and returns a JWT token if everything matches.
    Returns None if login fails.
    """
    user = await users_collection.find_one({"username": username})
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None

    # Password correct -> create a token containing the username and role
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}