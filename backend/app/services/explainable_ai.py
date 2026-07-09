# explainable_ai.py
# Instead of just giving a risk score, this generates the PLAIN-ENGLISH
# reasons WHY a particular log entry looks risky. This is what makes
# our AI "explainable" rather than a black box.

from app.ml.feature_engineering import extract_login_hour


def generate_reasons(log: dict) -> list[str]:
    """
    Looks at the raw fields of a log entry and returns a list of
    human-readable reasons explaining suspicious behavior.
    Returns an empty list if nothing looks unusual.
    """
    reasons = []

    hour = extract_login_hour(log["login_time"])
    if hour < 8 or hour > 20:
        reasons.append(f"Login at unusual time ({hour:02d}:00)")

    known_devices = ["Laptop-Win10", "Laptop-Win11", "Desktop-Office", "MacBook-Pro"]
    if log["device"] not in known_devices:
        reasons.append(f"Unknown or unregistered device used ({log['device']})")

    normal_locations = ["Mumbai-HQ", "Delhi-Branch", "Bangalore-Branch", "Chennai-Branch", "Remote-VPN"]
    if log["location"] not in normal_locations:
        reasons.append(f"Login from unusual location ({log['location']})")

    if int(log["failed_logins"]) >= 3:
        reasons.append(f"Multiple failed login attempts ({log['failed_logins']})")

    if int(log["files_downloaded"]) >= 100:
        reasons.append(f"Unusually high file downloads ({log['files_downloaded']} files)")

    usb = log["usb_connected"] in [True, "True", "true", 1]
    if usb:
        reasons.append("USB storage device connected")

    sensitive_dbs = ["Finance DB", "Payroll DB", "HR DB"]
    if log["database_access"] in sensitive_dbs:
        reasons.append(f"Accessed sensitive database ({log['database_access']})")

    admin = log["admin_access"] in [True, "True", "true", 1]
    if admin:
        reasons.append("Used administrator-level access")

    return reasons