# main.py
# This is the entry point of our FastAPI backend.
# Run it with: uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth_router,
    employee_router,
    logs_router,
    dashboard_router,
    risk_router,
    face_router,
    quantum_router,
    access_control_router,
    incident_router,
)

app = FastAPI(
    title="Sri-Guard API",
    description="Explainable AI-Powered Insider Threat Prevention Platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(employee_router.router)
app.include_router(logs_router.router)
app.include_router(dashboard_router.router)
app.include_router(risk_router.router)
app.include_router(face_router.router)
app.include_router(quantum_router.router)
app.include_router(access_control_router.router)
app.include_router(incident_router.router)


@app.get("/")
async def root():
    return {"message": "Sri-Guard API is running"}