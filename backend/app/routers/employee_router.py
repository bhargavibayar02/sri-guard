# employee_router.py
# Endpoints for listing, searching, and viewing employee profiles.

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from app.database.mongodb import employees_collection
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/")
async def get_employees(
    search: Optional[str] = Query(None, description="Search by name or employee_id"),
    department: Optional[str] = Query(None, description="Filter by department"),
    user=Depends(get_current_user)  # protects this route -- must be logged in
):
    """
    Returns the list of employees, optionally filtered by
    search text (name/id) and department.
    """
    query = {}

    if department:
        query["department"] = department

    if search:
        # Case-insensitive search on name OR employee_id
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"employee_id": {"$regex": search, "$options": "i"}}
        ]

    employees = []
    cursor = employees_collection.find(query)
    async for emp in cursor:
        emp["_id"] = str(emp["_id"])  # convert MongoDB's ObjectId to string for JSON
        employees.append(emp)

    return employees


@router.get("/{employee_id}")
async def get_employee_profile(employee_id: str, user=Depends(get_current_user)):
    """Returns a single employee's full profile."""
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee["_id"] = str(employee["_id"])
    return employee