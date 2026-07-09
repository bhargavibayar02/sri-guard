# logs_router.py
# Endpoints for viewing activity logs.

from fastapi import APIRouter, Depends, HTTPException
from app.database.mongodb import logs_collection
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/logs", tags=["Activity Logs"])


@router.get("/")
async def get_all_logs(user=Depends(get_current_user)):
    """Returns all activity logs, most recent first."""
    logs = []
    cursor = logs_collection.find().sort("login_time", -1)
    async for log in cursor:
        log["_id"] = str(log["_id"])
        logs.append(log)
    return logs


@router.get("/{employee_id}")
async def get_employee_logs(employee_id: str, user=Depends(get_current_user)):
    """Returns all logs belonging to one specific employee."""
    logs = []
    cursor = logs_collection.find({"employee_id": employee_id}).sort("login_time", -1)
    async for log in cursor:
        log["_id"] = str(log["_id"])
        logs.append(log)

    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this employee")
    return logs