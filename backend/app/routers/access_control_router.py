# access_control_router.py
# Endpoint that triggers the Risk-Based Access Control simulation
# for a given employee, based on their current risk_score.

from fastapi import APIRouter, Depends, HTTPException
from app.database.mongodb import employees_collection
from app.services.access_control import simulate_access_control
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/access", tags=["Risk-Based Access Control"])


@router.post("/simulate/{employee_id}")
async def simulate(employee_id: str, user=Depends(get_current_user)):
    """
    Looks up the employee's current risk_score and simulates the
    appropriate access control response (lock account, force MFA,
    notify SOC, generate incident) if risk is High or Critical.
    """
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    risk_score = employee.get("risk_score", 0)
    result = await simulate_access_control(employee_id, risk_score)
    return result