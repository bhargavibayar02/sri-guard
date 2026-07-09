# incident_service.py
# Builds a complete Incident object for an employee by combining:
# their worst (highest-risk) log entry, explainable AI reasons,
# MITRE mapping, threat timeline, and recommended action.

from datetime import datetime
from app.database.mongodb import logs_collection, employees_collection, incidents_collection
from app.services.threat_timeline import generate_timeline


def _recommend_action(risk_score: float) -> str:
    if risk_score >= 90:
        return "Lock account immediately, force MFA reset, escalate to SOC lead for investigation."
    elif risk_score >= 71:
        return "Force MFA re-authentication and monitor closely for further suspicious activity."
    elif risk_score >= 41:
        return "Flag for review during next routine security audit."
    else:
        return "No action required — behavior within normal parameters."


async def build_incident(employee_id: str, face_verification_result: str = "Not Performed") -> dict:
    """
    Builds and saves a complete Incident record for the given employee,
    based on their highest-risk log entry.
    """
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        return None

    # Find this employee's single highest-risk log entry
    worst_log = await logs_collection.find_one(
        {"employee_id": employee_id},
        sort=[("risk_score", -1)]
    )

    if not worst_log:
        return None

    risk_score = worst_log.get("risk_score", 0) or 0
    reasons = worst_log.get("risk_reasons", [])
    mitre_mapping = worst_log.get("mitre_tags", [])
    timeline = generate_timeline(worst_log)

    incident = {
        "employee_id": employee_id,
        "department": employee.get("department", "Unknown"),
        "risk_score": risk_score,
        "reasons": reasons,
        "timeline": timeline,
        "mitre_mapping": mitre_mapping,
        "face_verification_result": face_verification_result,
        "recommended_action": _recommend_action(risk_score),
        "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    }

    # Save to MongoDB and attach the generated _id back onto the dict
    insert_result = await incidents_collection.insert_one(incident)
    incident["_id"] = str(insert_result.inserted_id)

    return incident