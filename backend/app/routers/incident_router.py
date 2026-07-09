# incident_router.py
# Endpoints to generate an Incident Report and download it as a PDF.

import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from bson import ObjectId
from app.database.mongodb import incidents_collection
from app.services.incident_service import build_incident
from app.services.pdf_generator import generate_incident_pdf
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/incident", tags=["Incident Report"])


@router.post("/generate/{employee_id}")
async def generate_incident(
    employee_id: str,
    face_verification_result: str = "Not Performed",
    user=Depends(get_current_user)
):
    """
    Builds and saves a complete Incident record for this employee,
    based on their highest-risk log entry. Optionally pass in a
    face_verification_result string from the Face Verify step.
    """
    incident = await build_incident(employee_id, face_verification_result)
    if not incident:
        raise HTTPException(status_code=404, detail="No log data found for this employee")
    return incident


@router.get("/{incident_id}")
async def get_incident(incident_id: str, user=Depends(get_current_user)):
    """Fetches a previously generated incident by its ID."""
    incident = await incidents_collection.find_one({"_id": ObjectId(incident_id)})
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident["_id"] = str(incident["_id"])
    return incident


@router.get("/{incident_id}/pdf")
async def download_incident_pdf(incident_id: str, user=Depends(get_current_user)):
    """Generates (or regenerates) the PDF for this incident and returns it as a download."""
    incident = await incidents_collection.find_one({"_id": ObjectId(incident_id)})
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident["_id"] = str(incident["_id"])

    pdf_path = generate_incident_pdf(incident)
    filename = f"Sri-Guard_Incident_{incident['employee_id']}.pdf"

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=filename
    )