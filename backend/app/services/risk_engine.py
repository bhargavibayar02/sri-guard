# risk_engine.py
# The core "brain" of Sri-Guard. Loads the trained Isolation Forest model,
# scores ALL logs together (as a batch), and converts raw anomaly scores
# into a 0-100 risk scale using PERCENTILE RANKING -- this guarantees a
# natural spread across Safe/Medium/High/Critical instead of everything
# clustering at one extreme.

import os
import joblib
import numpy as np
import pandas as pd
from app.ml.feature_engineering import build_feature_row
from app.services.explainable_ai import generate_reasons
from app.services.mitre_mapper import map_reasons_to_mitre

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "model.pkl")

try:
    _model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    _model = None
    print("WARNING: model.pkl not found. Run `python app/ml/train_model.py` first.")


def classify_risk(score: float) -> str:
    if score <= 40:
        return "Safe"
    elif score <= 70:
        return "Medium"
    elif score <= 90:
        return "High"
    else:
        return "Critical"


def analyze_log(log: dict) -> dict:
    """
    Analyzes a SINGLE log entry (used for one-off / real-time checks).
    NOTE: for scoring the whole database at once, use analyze_all_logs()
    below instead -- it produces a much better spread of risk scores.
    """
    reasons = generate_reasons(log)
    mitre_tags = map_reasons_to_mitre(reasons)

    # Simple rule-based score for single-log analysis:
    # each reason found adds 15 points, capped at 100.
    risk_score = min(100, len(reasons) * 15)
    risk_level = classify_risk(risk_score)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons,
        "mitre_tags": mitre_tags,
    }


def analyze_all_logs(logs: list[dict]) -> list[dict]:
    """
    Analyzes ALL log entries together as a batch. This is the function
    the /risk/analyze endpoint should use.

    Why batch scoring matters: Isolation Forest's raw score_samples()
    output has no fixed meaning on its own -- a score of -0.05 could be
    "very anomalous" in one dataset and "totally normal" in another.
    So instead of guessing a fixed range, we RANK every log against every
    OTHER log in this batch, and convert that rank into a 0-100 percentile.
    This guarantees roughly the top 10% land as High/Critical, matching
    how our dummy dataset was generated (90% normal / 10% suspicious).
    """
    results = []

    if _model is None or len(logs) == 0:
        # Fallback: no trained model available, use rule-based scoring for each
        for log in logs:
            results.append(analyze_log(log))
        return results

    # Step 1: Build numeric features for every log at once
    feature_rows = [build_feature_row(log) for log in logs]
    features_df = pd.DataFrame(feature_rows)

    # Step 2: Get raw anomaly scores from the model for the WHOLE batch
    # (higher score_samples() = more normal, lower = more anomalous)
    raw_scores = _model.score_samples(features_df)

    # Step 3: Convert raw scores into percentile ranks (0-100).
    # We INVERT so that the most anomalous log (lowest raw score) gets
    # the HIGHEST risk percentile (closest to 100).
    # pandas' rank(pct=True) handles ties gracefully and spreads scores
    # evenly across the full 0-100 range.
    scores_series = pd.Series(raw_scores)
    # rank ascending=True means lowest raw_score (most anomalous) gets rank 1
    # we want that to become risk=100, so we invert with (1 - pct_rank)
    percentile_ranks = scores_series.rank(pct=True, ascending=True)
    risk_scores = (1 - percentile_ranks) * 100

    # Step 4: Combine with reasons + MITRE mapping for each log
    for i, log in enumerate(logs):
        reasons = generate_reasons(log)
        mitre_tags = map_reasons_to_mitre(reasons)
        risk_score = round(float(risk_scores.iloc[i]), 1)
        risk_level = classify_risk(risk_score)

        results.append({
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reasons": reasons,
            "mitre_tags": mitre_tags,
        })

    return results