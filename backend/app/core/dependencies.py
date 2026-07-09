# app/core/dependencies.py
# Handles JWT authentication for protected routes and enables
# the Swagger "Authorize" button.

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token

# Creates the OpenAPI security scheme so Swagger shows "Authorize"
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Validates the JWT token sent in the Authorization header.

    Expected header:
        Authorization: Bearer <jwt_token>

    Returns:
        Decoded JWT payload:
        {
            "sub": "<username>",
            "role": "<role>"
        }

    Raises:
        401 if the token is missing, invalid, or expired.
    """

    # Extract the JWT token
    token = credentials.credentials

    # Decode and verify it
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    return payload