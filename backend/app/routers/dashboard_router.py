# dashboard_router.py
# Powers the main dashboard summary numbers and graphs.
# NOTE: risk_score fields are populated by the ML engine in Phase 5.
# Until then, this will show all employees as "Safe" (risk_score = 0),
# which is expected -- Phase 9 wires this fully together.

from fastapi import APIRouter, Depends
from app.database.mongodb import employees_collection, logs_collection
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def classify_risk(score: float) -> str:
    """Converts a numeric risk score into a risk category label."""
    if score <= 40:
        return "Safe"
    elif score <= 70:
        return "Medium"
    elif score <= 90:
        return "High"
    else:
        return "Critical"


@router.get("/summary")
async def get_dashboard_summary(user=Depends(get_current_user)):
    """
    Returns the counts needed for the dashboard cards:
    Total Employees, Safe, Medium, High, Critical, Critical Alerts.
    """
    total_employees = await employees_collection.count_documents({})

    # Count employees by risk level (stored on the employee record)
    safe = await employees_collection.count_documents({"risk_level": "Safe"})
    medium = await employees_collection.count_documents({"risk_level": "Medium"})
    high = await employees_collection.count_documents({"risk_level": "High"})
    critical = await employees_collection.count_documents({"risk_level": "Critical"})

    return {
        "total_employees": total_employees,
        "safe": safe,
        "medium": medium,
        "high": high,
        "critical": critical,
        "critical_alerts": critical  # for MVP, critical alerts == critical-risk employees
    }


@router.get("/department-risk")
async def get_department_risk(user=Depends(get_current_user)):
    """
    Returns average risk score grouped by department,
    used for the 'Department Wise Risk' bar chart.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "avg_risk": {"$avg": "$risk_score"},
                "employee_count": {"$sum": 1}
            }
        }
    ]
    results = []
    async for row in employees_collection.aggregate(pipeline):
        results.append({
            "department": row["_id"],
            "avg_risk": round(row["avg_risk"] or 0, 1),
            "employee_count": row["employee_count"]
        })
    return results


@router.get("/recent-alerts")
async def get_recent_alerts(user=Depends(get_current_user)):
    """Returns the most recent high/critical risk log entries."""
    alerts = []
    cursor = logs_collection.find(
        {"risk_score": {"$gte": 71}}
    ).sort("login_time", -1).limit(10)

    async for log in cursor:
        log["_id"] = str(log["_id"])
        alerts.append(log)

    return alerts