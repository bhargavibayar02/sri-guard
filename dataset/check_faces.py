# check_faces.py
# Scans all downloaded "face" images and reports which ones are
# actually valid images vs broken/corrupted files.
#
# Run with: python check_faces.py   (from inside dataset/)

import os
from PIL import Image

FACES_DIR = "registered_faces"

def main():
    files = [f for f in os.listdir(FACES_DIR) if f.endswith(".jpg")]
    print(f"Checking {len(files)} files...\n")

    valid = 0
    broken = []

    for filename in files:
        path = os.path.join(FACES_DIR, filename)
        try:
            img = Image.open(path)
            img.verify()  # checks the file is a real, uncorrupted image
            valid += 1
        except Exception:
            broken.append(filename)

    print(f"Valid images: {valid}")
    print(f"Broken images: {len(broken)}")
    if broken:
        print("\nBroken files:")
        for f in broken[:20]:  # show first 20
            print(f"  - {f}")
        if len(broken) > 20:
            print(f"  ... and {len(broken) - 20} more")

if __name__ == "__main__":
    main()