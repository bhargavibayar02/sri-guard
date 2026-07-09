# face_verification.py
# Compares a captured webcam image against an employee's registered
# photo using DeepFace. Only called for CRITICAL risk events (>=90).

import os
import traceback
from deepface import DeepFace

REGISTERED_FACES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "dataset", "registered_faces"
)

# Log file to guarantee we capture the full error, even if terminal
# output gets buffered or hidden by uvicorn's reload subprocess.
ERROR_LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "face_verify_error.log")


def verify_face(employee_id: str, captured_image_path: str) -> dict:
    registered_path = os.path.join(REGISTERED_FACES_DIR, f"{employee_id}.jpg")

    if not os.path.exists(registered_path):
        return {
            "verified": False,
            "distance": None,
            "message": f"No registered photo found for employee {employee_id}."
        }

    try:
        result = DeepFace.verify(
            img1_path=captured_image_path,
            img2_path=registered_path,
            model_name="Facenet",
            enforce_detection=False,
        )

        if result["verified"]:
            message = "Identity Verified — face matches registered employee photo."
        else:
            message = "Possible Account Compromise — face does NOT match registered photo."

        return {
            "verified": result["verified"],
            "distance": round(result["distance"], 4),
            "message": message,
        }

    except Exception as e:
        # Write the FULL traceback to a log file we can definitely find,
        # regardless of terminal buffering issues.
        with open(ERROR_LOG_PATH, "w") as log_file:
            log_file.write(f"captured_image_path: {captured_image_path}\n")
            log_file.write(f"registered_path: {registered_path}\n")
            log_file.write(f"captured exists: {os.path.exists(captured_image_path)}\n")
            log_file.write(f"registered exists: {os.path.exists(registered_path)}\n\n")
            log_file.write("FULL TRACEBACK:\n")
            log_file.write(traceback.format_exc())

        return {
            "verified": False,
            "distance": None,
            "message": f"Face verification could not be completed: {str(e)}"
        }