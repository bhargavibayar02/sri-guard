# employee_model.py
# Defines the structure of an Employee record.

from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    employee_id: str          # e.g. "EMP001"
    name: str
    department: str           # e.g. "Finance", "IT", "HR"
    role: str                 # e.g. "Analyst", "Manager"
    normal_working_hours: str # e.g. "09:00-18:00"
    registered_face_path: Optional[str] = None  # path to their photo file
    risk_level: Optional[str] = "Safe"          # Safe / Medium / High / Critical
    risk_score: Optional[float] = 0.0