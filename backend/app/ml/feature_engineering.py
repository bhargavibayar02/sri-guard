# feature_engineering.py
# Converts raw, human-readable log columns (like "device: Laptop-Win10")
# into pure NUMBERS, because Isolation Forest (and all ML models) can
# only do math on numbers, not text.

import pandas as pd
from datetime import datetime

KNOWN_DEVICES = ["Laptop-Win10", "Laptop-Win11", "Desktop-Office", "MacBook-Pro"]
NORMAL_LOCATIONS = ["Mumbai-HQ", "Delhi-Branch", "Bangalore-Branch", "Chennai-Branch", "Remote-VPN"]
SENSITIVE_DATABASES = ["Finance DB", "Payroll DB", "HR DB"]


def extract_login_hour(login_time_str: str) -> int:
    """Pulls just the hour (0-23) out of a full datetime string."""
    dt = pd.to_datetime(login_time_str)
    return dt.hour


def is_unusual_hour(hour: int) -> int:
    """Returns 1 if login happened outside typical 8 AM - 8 PM working window."""
    return 1 if (hour < 8 or hour > 20) else 0


def is_known_device(device: str) -> int:
    """Returns 1 if this is a registered/known company device, else 0."""
    return 1 if device in KNOWN_DEVICES else 0


def is_known_location(location: str) -> int:
    """Returns 1 if login came from a normal office/VPN location."""
    return 1 if location in NORMAL_LOCATIONS else 0


def is_sensitive_db(db_access: str) -> int:
    """Returns 1 if the database accessed is a sensitive one."""
    return 1 if db_access in SENSITIVE_DATABASES else 0


def build_feature_row(log: dict) -> dict:
    """
    Takes ONE raw log entry (a dict) and returns a dict of pure numeric
    features that the ML model can understand.
    """
    hour = extract_login_hour(log["login_time"])

    return {
        "unusual_hour": is_unusual_hour(hour),
        "unknown_device": 1 - is_known_device(log["device"]),
        "unknown_location": 1 - is_known_location(log["location"]),
        "failed_logins": int(log["failed_logins"]),
        "files_downloaded": int(log["files_downloaded"]),
        "usb_connected": 1 if log["usb_connected"] in [True, "True", "true", 1] else 0,
        "sensitive_db_access": is_sensitive_db(log["database_access"]),
        "admin_access": 1 if log["admin_access"] in [True, "True", "true", 1] else 0,
    }


def build_feature_dataframe(logs_df: pd.DataFrame) -> pd.DataFrame:
    """Applies build_feature_row() to an entire DataFrame of logs at once."""
    feature_rows = []
    for _, row in logs_df.iterrows():
        feature_rows.append(build_feature_row(row.to_dict()))
    return pd.DataFrame(feature_rows)