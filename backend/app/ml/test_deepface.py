# test_deepface.py
# A tiny standalone script to confirm DeepFace + TensorFlow installed
# correctly, BEFORE we build the real face verification feature.
# It downloads a small pre-trained face-recognition model on first run
# (one-time internet download, cached afterward).
#
# Run with: python app/ml/test_deepface.py

from deepface import DeepFace

print("DeepFace imported successfully.")
print("Testing model load (this downloads weights on first run, ~100MB)...")

# This just verifies the underlying face-recognition model loads without
# crashing -- we're not comparing real images yet, just confirming setup.
try:
    DeepFace.build_model("Facenet")
    print("SUCCESS: DeepFace model loaded correctly. Face verification is ready to use.")
except Exception as e:
    print("ERROR loading DeepFace model:")
    print(e)