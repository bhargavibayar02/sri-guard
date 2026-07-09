# train_model.py
# Trains an Isolation Forest model on employee_logs.csv and saves it
# to model.pkl, so the live API can reuse it without retraining every time.
#
# Run with: python app/ml/train_model.py   (from inside backend/)

import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
import sys
import os

# Allow importing from app/ when running this script directly
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from app.ml.feature_engineering import build_feature_dataframe

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "dataset", "employee_logs.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def train():
    print("Loading dataset from:", DATASET_PATH)
    logs_df = pd.read_csv(DATASET_PATH)
    print(f"Loaded {len(logs_df)} log entries.")

    # Convert raw logs into numeric features
    features_df = build_feature_dataframe(logs_df)
    print("Feature columns:", list(features_df.columns))

    # Isolation Forest: an algorithm that isolates "outlier" data points
    # by randomly splitting the data -- outliers get isolated in FEWER
    # splits than normal points, which is how it detects anomalies.
    #
    # contamination=0.10 tells the model "expect about 10% of the data
    # to be anomalies" -- matches how we generated our dummy dataset.
    model = IsolationForest(
        n_estimators=150,
        contamination=0.10,
        random_state=42
    )
    model.fit(features_df)

    # Save the trained model to disk so we don't retrain on every API call
    joblib.dump(model, MODEL_PATH)
    print(f"Model trained and saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train()