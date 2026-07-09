# quantum_router.py
# Exposes the quantum-safe credential protection demo as API endpoints.

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.quantum_safe import quantum_safe_encrypt, get_quantum_safe_status
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/quantum", tags=["Quantum-Safe Credential Protection"])


class EncryptRequest(BaseModel):
    credential: str  # the admin credential text to demo-encrypt


@router.get("/status")
async def quantum_status(user=Depends(get_current_user)):
    """Returns whether real post-quantum encryption (liboqs) is available or simulated."""
    return get_quantum_safe_status()


@router.post("/encrypt-demo")
async def encrypt_demo(request: EncryptRequest, user=Depends(get_current_user)):
    """
    Demonstrates quantum-safe encryption on a given admin credential string.
    Uses real liboqs (Kyber512) if available, otherwise a clearly-labeled
    simulation. This is for DEMONSTRATION purposes only, as required by
    the MVP spec -- never encrypts real production secrets this way.
    """
    result = quantum_safe_encrypt(request.credential)
    return result