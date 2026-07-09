# access_control.py
# Simulates Risk-Based Access Control actions for CRITICAL risk employees
# (risk_score >= 90). This is an MVP SIMULATION -- it does not actually
# lock any real account or send real MFA prompts, but it demonstrates
# exactly what a production system would trigger automatically.

from datetime import datetime
from app.database.mongodb import alerts_collection, employees_collection


async def simulate_access_control(employee_id: str, risk_score: float) -> dict:
    """
    Given an employee's current risk score, simulates the appropriate
    access control response. Only triggers "critical" actions at >=90.
    Also logs an Alert record in MongoDB so it shows up on the dashboard.
    """
    if risk_score >= 90:
        actions = {
            "account_locked": True,
            "mfa_forced": True,
            "soc_notified": True,
            "incident_generated": True,
        }
        severity = "Critical"
    elif risk_score >= 71:
        actions = {
            "account_locked": False,
            "mfa_forced": True,
            "soc_notified": True,
            "incident_generated": False,
        }
        severity = "High"
    else:
        actions = {
            "account_locked": False,
            "mfa_forced": False,
            "soc_notified": False,
            "incident_generated": False,
        }
        severity = "Normal"

    # Record this as an alert so it's visible on the dashboard's
    # "Recent Alerts" list and for audit history.
    alert_record = {
        "employee_id": employee_id,
        "risk_score": risk_score,
        "severity": severity,
        "actions_taken": actions,
        "timestamp": datetime.utcnow().isoformat(),
    }
    await alerts_collection.insert_one(alert_record)

    return {
        "employee_id": employee_id,
        "risk_score": risk_score,
        "severity": severity,
        "actions": actions,
        "message": _build_message(severity, actions),
    }


def _build_message(severity: str, actions: dict) -> str:
    """Builds a plain-English summary of what was simulated."""
    if severity == "Critical":
        return (
            "CRITICAL RISK DETECTED. Simulated actions: account locked, "
            "multi-factor authentication forced, SOC team notified, "
            "incident report generated. Identity verification required."
        )
    elif severity == "High":
        return (
            "High risk detected. Simulated actions: multi-factor authentication "
            "forced, SOC team notified."
        )
    else:
        return "Risk within normal range. No access control action required."