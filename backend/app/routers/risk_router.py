# risk_router.py
# Endpoint that runs the Risk Engine over ALL logs in the database,
# updates each log with its risk score/reasons/mitre tags, and updates
# each employee's overall risk_level too.

from fastapi import APIRouter, Depends
from app.database.mongodb import logs_collection, employees_collection
from app.services.risk_engine import analyze_all_logs
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/risk", tags=["Risk Engine"])


@router.post("/analyze")
async def analyze_all(user=Depends(get_current_user)):
    """
    Runs AI risk analysis on every log entry in the database, scoring
    them all TOGETHER (batch) so risk scores naturally spread across
    Safe/Medium/High/Critical instead of clustering at one extreme.
    """
    # Step 1: Load every log entry into memory
    all_logs = []
    cursor = logs_collection.find({})
    async for log in cursor:
        all_logs.append(log)

    if not all_logs:
        return {"message": "No logs found to analyze", "logs_analyzed": 0, "employees_updated": 0}

    # Step 2: Run batch analysis (this is the key fix -- scores ALL logs
    # relative to each other, instead of one at a time)
    results = analyze_all_logs(all_logs)

    # Step 3: Update each log entry in MongoDB with its analysis
    employee_max_risk = {}
    for log, result in zip(all_logs, results):
        await logs_collection.update_one(
            {"_id": log["_id"]},
            {"$set": {
                "risk_score": result["risk_score"],
                "risk_reasons": result["reasons"],
                "mitre_tags": result["mitre_tags"],
            }}
        )

        emp_id = log["employee_id"]
        current_max = employee_max_risk.get(emp_id, 0)
        if result["risk_score"] > current_max:
            employee_max_risk[emp_id] = result["risk_score"]

    # Step 4: Update each employee's overall risk_level based on their
    # HIGHEST-risk log entry (worst-case behavior wins)
    for emp_id, max_score in employee_max_risk.items():
        level = (
            "Critical" if max_score > 90 else
            "High" if max_score > 70 else
            "Medium" if max_score > 40 else
            "Safe"
        )
        await employees_collection.update_one(
            {"employee_id": emp_id},
            {"$set": {"risk_score": round(max_score, 1), "risk_level": level}}
        )

    return {
        "message": "Risk analysis complete",
        "logs_analyzed": len(all_logs),
        "employees_updated": len(employee_max_risk)
    }