# incident_model.py
# Defines the structure of a generated Incident Report.

from pydantic import BaseModel
from typing import List, Optional

class Incident(BaseModel):
    employee_id: str
    department: str
    risk_score: float
    reasons: List[str]
    timeline: List[str]
    mitre_mapping: List[str]
    face_verification_result: Optional[str] = "Not Performed"
    recommended_action: str
    created_at: str