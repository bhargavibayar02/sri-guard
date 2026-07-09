# face_router.py
# Endpoint that accepts a webcam-captured image (uploaded as a file)
# and compares it against the employee's registered photo.

import os
import uuid
from io import BytesIO
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.services.face_verification import verify_face
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/face", tags=["Face Verification"])

TEMP_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "temp_uploads")
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)


@router.post("/verify/{employee_id}")
async def verify_employee_face(
    employee_id: str,
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    """
    Accepts a webcam-captured image file, RE-ENCODES it as a clean JPEG
    using Pillow (this fixes format/encoding mismatches from browser
    canvas captures), saves it temporarily, compares it against the
    employee's registered photo using DeepFace, then deletes the file.
    """
    temp_filename = f"{uuid.uuid4()}.jpg"
    temp_path = os.path.join(TEMP_UPLOAD_DIR, temp_filename)

    try:
        # Read the raw uploaded bytes
        contents = await file.read()

        # Re-encode using Pillow to guarantee a clean, standard JPEG file --
        # this fixes issues where browser-captured images have unusual
        # encoding/color modes (e.g. RGBA) that OpenCV/DeepFace can't read.
        img = Image.open(BytesIO(contents))
        img = img.convert("RGB")  # drop alpha channel if present
        img.save(temp_path, "JPEG")

        result = verify_face(employee_id, temp_path)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Face verification failed: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)