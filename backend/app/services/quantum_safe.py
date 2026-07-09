# quantum_safe.py
# Demonstrates POST-QUANTUM cryptography awareness by encrypting admin
# credentials using Open Quantum Safe (liboqs) if it's installed.
#
# WHY THIS MATTERS: today's encryption (RSA, ECC) relies on math problems
# that are hard for normal computers but WILL be breakable by future
# quantum computers. Post-quantum cryptography uses different math
# problems believed to resist quantum attacks too. Banks and governments
# are already starting to prepare for this transition -- this module
# demonstrates that awareness.
#
# FALLBACK: liboqs has tricky native (C library) dependencies that often
# fail to install on Windows via pip alone. If it's unavailable, we
# CLEARLY label the output as a simulation, never pretending otherwise.

import base64
import hashlib
import os

# Try to import the real Open Quantum Safe library
try:
    import oqs
    OQS_AVAILABLE = True
except ImportError:
    OQS_AVAILABLE = False


def encrypt_with_oqs(plaintext: str) -> dict:
    """
    Uses a real post-quantum key encapsulation mechanism (Kyber, the
    NIST-selected standard for post-quantum key exchange) to demonstrate
    quantum-safe encryption.
    """
    # Kyber512 is a NIST-standardized post-quantum key encapsulation
    # algorithm -- resistant to attacks from quantum computers, unlike
    # today's RSA/ECC encryption.
    with oqs.KeyEncapsulation("Kyber512") as kem:
        public_key = kem.generate_keypair()
        ciphertext, shared_secret = kem.encap_secret(public_key)

        # Use the quantum-safe shared secret to actually encrypt our data
        # (simple XOR demo -- in production you'd use AES with this secret)
        key_bytes = shared_secret[:32]
        plaintext_bytes = plaintext.encode()
        encrypted_bytes = bytes(
            b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(plaintext_bytes)
        )

        return {
            "mode": "REAL_QUANTUM_SAFE",
            "algorithm": "Kyber512 (NIST Post-Quantum Standard)",
            "encrypted_data": base64.b64encode(encrypted_bytes).decode(),
            "public_key_preview": base64.b64encode(public_key[:32]).decode() + "...",
            "note": "Encrypted using a real post-quantum key encapsulation mechanism (liboqs)."
        }


def encrypt_simulated(plaintext: str) -> dict:
    """
    FALLBACK simulation used when liboqs isn't installed.
    Clearly labeled as a simulation -- NOT real post-quantum cryptography.
    Uses a simple, reversible encoding just to demonstrate the CONCEPT
    of how quantum-safe encryption would be applied to admin credentials.
    """
    # A simple, clearly-fake "encryption" for demo purposes only --
    # combines a random salt with a SHA3-512 hash (SHA3 is a NIST standard
    # that is itself believed to be quantum-resistant, even though this
    # simulation doesn't perform real post-quantum key exchange).
    salt = os.urandom(16)
    combined = salt + plaintext.encode()
    digest = hashlib.sha3_512(combined).hexdigest()

    return {
        "mode": "SIMULATED",
        "algorithm": "SHA3-512 based simulation (NOT a real post-quantum KEM)",
        "encrypted_data": digest,
        "salt": base64.b64encode(salt).decode(),
        "note": (
            "⚠️ MVP DEMONSTRATION ONLY. Open Quantum Safe (liboqs) is not "
            "installed in this environment. This is a SIMULATED representation "
            "of quantum-safe encryption for demo purposes -- it does NOT provide "
            "real post-quantum security guarantees. In production, this would "
            "be replaced with a real Kyber/Dilithium implementation via liboqs."
        )
    }


def quantum_safe_encrypt(plaintext: str) -> dict:
    """
    Main entry point. Automatically uses real liboqs if available,
    otherwise clearly falls back to a labeled simulation.
    """
    if OQS_AVAILABLE:
        try:
            return encrypt_with_oqs(plaintext)
        except Exception as e:
            # If liboqs is installed but fails at runtime for any reason,
            # fall back to simulation rather than crashing the demo.
            result = encrypt_simulated(plaintext)
            result["fallback_reason"] = f"liboqs installed but failed at runtime: {str(e)}"
            return result
    else:
        return encrypt_simulated(plaintext)


def get_quantum_safe_status() -> dict:
    """Returns whether real post-quantum encryption is active or simulated."""
    return {
        "oqs_available": OQS_AVAILABLE,
        "status": "REAL_QUANTUM_SAFE_ACTIVE" if OQS_AVAILABLE else "SIMULATION_MODE",
        "message": (
            "Open Quantum Safe (liboqs) is installed and active."
            if OQS_AVAILABLE else
            "Open Quantum Safe (liboqs) is not installed. Running in simulation mode for MVP demo purposes."
        )
    }