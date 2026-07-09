# generate_faces.py
# Generates registered face images locally using a REAL, small set of
# diverse sample face photos bundled with the popular 'opencv' and
# 'face_recognition' test datasets -- avoids relying on an external
# website that can rate-limit or block automated requests.
#
# Approach: we use a curated set of public-domain / CC0 face photos
# from Unsplash Source or generate consistent placeholder faces using
# a local face-generation library.
#
# For MVP reliability, this version downloads from a MORE STABLE
# source (randomuser.me API, which returns real profile-style photos
# and is far less likely to rate-limit or block automated scripts
# than thispersondoesnotexist.com).
#
# Run with: python generate_faces.py   (from inside dataset/)

import os
import csv
import time
import requests
from PIL import Image
from io import BytesIO

FACES_DIR = "registered_faces"
EMPLOYEES_CSV = "employees.csv"


def download_and_validate_face(save_path: str, seed: int, retries: int = 3) -> bool:
    """
    Downloads one face photo from randomuser.me (a stable, reliable API
    that returns real photo-style headshots for testing purposes) and
    VALIDATES it's a proper image before saving.
    """
    # randomuser.me lets us request a specific "seed" so re-runs are consistent,
    # and returns a real JPEG photo URL for a fake user profile.
    api_url = f"https://randomuser.me/api/?seed={seed}&inc=picture"

    for attempt in range(retries):
        try:
            api_response = requests.get(api_url, timeout=15)
            api_response.raise_for_status()
            data = api_response.json()
            photo_url = data["results"][0]["picture"]["large"]

            image_response = requests.get(photo_url, timeout=15)
            image_response.raise_for_status()

            # VALIDATE before saving -- this is the key fix
            img = Image.open(BytesIO(image_response.content))
            img.verify()  # raises an exception if not a real image

            # Re-open (verify() invalidates the file handle) and save properly
            img = Image.open(BytesIO(image_response.content))
            img.convert("RGB").save(save_path, "JPEG")
            return True

        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(1)

    return False


def main():
    os.makedirs(FACES_DIR, exist_ok=True)

    with open(EMPLOYEES_CSV, newline="") as f:
        reader = csv.DictReader(f)
        employees = list(reader)

    print(f"Downloading {len(employees)} validated face images...")
    print("(Using randomuser.me -- stable, reliable source)\n")

    success_count = 0
    for i, emp in enumerate(employees):
        emp_id = emp["employee_id"]
        save_path = os.path.join(FACES_DIR, f"{emp_id}.jpg")

        print(f"{emp_id}: downloading...")
        if download_and_validate_face(save_path, seed=i):
            success_count += 1
            print(f"{emp_id}: OK")
        else:
            print(f"{emp_id}: FAILED after retries.")

        time.sleep(0.3)

    print(f"\nDone. {success_count}/{len(employees)} valid face images saved to {FACES_DIR}/")


if __name__ == "__main__":
    main()