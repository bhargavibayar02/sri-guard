# log_model.py
# Defines the structure of one activity log entry
# (matches the columns in employee_logs.csv).

from pydantic import BaseModel
from typing import Optional, List

class LogEntry(BaseModel):
    employee_id: str
    login_time: str           # ISO datetime string
    device: str
    ip_address: str
    failed_logins: int
    files_downloaded: int
    usb_connected: bool
    database_access: str      # e.g. "None", "Finance DB", "HR DB"
    admin_access: bool
    location: str

    # These fields get filled in AFTER the ML model runs (Phase 5)
    risk_score: Optional[float] = None
    risk_reasons: Optional[List[str]] = []
    mitre_tags: Optional[List[str]] = []