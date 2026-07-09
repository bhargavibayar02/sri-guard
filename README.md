Sri-Guard

Explainable AI-Powered Insider Threat Prevention Platform with Risk-Adaptive Access Control and Quantum-Safe Credential Protection

Built for the Finspark Hackathon 2026


Problem Statement

Insider threats — from employees, contractors, vendors, and admins — acting maliciously, negligently, or under compromise pose serious risk to banking security and data integrity. Sri-Guard was built to detect privileged access misuse before it becomes a breach.

Focus Areas


Insider Threat Detection
Behaviour Analytics
Privileged Access Management
Risk-Based Authentication
Quantum-Safe Security



What Sri-Guard Does

Unlike traditional insider-threat tools that output a single opaque risk score, Sri-Guard is built to be explainable end-to-end:


Detects misuse of privileged accounts and identifies insider threats in real time using AI-driven behavioural analysis (Isolation Forest anomaly detection).
Explains every flagged event in plain English (e.g. "Login at unusual time," "USB device connected," "Accessed Finance DB") instead of a black-box score.
Maps each reason to real MITRE ATT&CK techniques, making alerts SOC-analyst ready out of the box.
Reconstructs a chronological Threat Timeline for every flagged session.
Simulates Risk-Based Access Control — locking the account, forcing MFA, and notifying the SOC team when risk crosses a critical threshold.
Verifies identity via webcam-based Face Verification (DeepFace), triggered only at Critical risk — never continuous surveillance.
Generates a downloadable PDF Incident Report containing the full investigation trail: risk score, reasons, timeline, MITRE mapping, and verification outcome.
Demonstrates Quantum-Safe Credential Protection — encrypting sensitive credentials using post-quantum cryptography (Kyber, NIST-standardized), with a clearly labeled simulation fallback where native quantum-safe libraries aren't available.


Tech Stack

LayerTechnologyFrontendReact, Tailwind CSS, Chart.jsBackendFastAPI (Python)DatabaseMongoDB (Atlas)Machine LearningPython, Pandas, Scikit-learn (Isolation Forest)Face VerificationDeepFace, OpenCVAuthenticationJWT, bcryptPDF ReportsReportLabQuantum-Safe CryptoOpen Quantum Safe (liboqs) — with simulated fallbackDeploymentVercel (frontend), Render (backend), MongoDB Atlas (database)


Architecture

┌─────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                        │
│   React + Tailwind + Chart.js  (SOC Analyst Dashboard)       │
└───────────────────────────┬───────────────────────────────────┘
                            │  REST API calls (JWT token in header)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND (Python)                 │
│                                                                │
│  Auth Module   │  Employee & Logs   │  Risk Engine            │
│  Explainable AI │  MITRE Mapper     │  Access Control (sim.)  │
│  Face Verify    │  Quantum-Safe     │  PDF Incident Report    │
└───────────────────────────┬───────────────────────────────────┘
                            │  Motor / PyMongo driver
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     MongoDB (Atlas or local)                 │
│  Collections: users, employees, logs, incidents, alerts      │
└─────────────────────────────────────────────────────────────┘

Data Flow:
Browser (Dashboard) → FastAPI (JWT-secured REST API) → Risk Engine + Explainable AI + MITRE Mapper → MongoDB → Incident PDF


Folder Structure

sri-guard/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── core/                    # Config, security (JWT/bcrypt), dependencies
│   │   ├── database/                # MongoDB connection
│   │   ├── models/                  # Pydantic schemas
│   │   ├── routers/                 # API endpoints (auth, employees, logs, risk, face, quantum, access, incident)
│   │   ├── services/                # Business logic (risk engine, explainable AI, MITRE mapper, face verification, quantum-safe, PDF generator)
│   │   └── ml/                      # Feature engineering + Isolation Forest training
│   ├── seed/                        # Scripts to seed admin user, dataset, and indexes
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/                   # Login, Dashboard, Employees, Logs, Face Verify, Quantum-Safe Demo
│   │   ├── components/              # Reusable UI (charts, tables, badges, timeline)
│   │   ├── api/                     # Axios client with JWT interceptor
│   │   └── context/                 # Auth context
│   └── package.json
│
├── dataset/
│   ├── employees.csv                # 100 dummy employees (banking roles)
│   ├── employee_logs.csv            # Activity logs (90% normal / 10% suspicious)
│   └── registered_faces/            # Synthetic reference photos for face verification
│
└── docs/                            # Architecture notes, pitch deck, demo script


Prerequisites


Python 3.11
Node.js 18+
MongoDB (local instance or MongoDB Atlas)
A webcam (for the Face Verification demo)



🚀 Getting Started

1. Clone the repository

bashgit clone https://github.com/YOUR_USERNAME/sri-guard.git
cd sri-guard

2. Backend setup

bashcd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

Create a .env file in backend/:

envMONGO_URI=mongodb://localhost:27017
DB_NAME=sriguard
JWT_SECRET=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

3. Generate the dataset

bashcd ../dataset
python generate_dataset.py
python generate_faces.py
cd ../backend

4. Seed the database and train the model

bashpython seed/create_admin.py
python seed/seed_data.py
python seed/create_indexes.py
python app/ml/train_model.py

5. Run the backend

bashuvicorn app.main:app --reload

API docs available at: http://127.0.0.1:8000/docs

6. Run the frontend

bashcd ../frontend
npm install
npm run dev

App available at: http://localhost:5173

7. Log in

Username: admin
Password: admin123

8. Run risk analysis

In Swagger (/docs), authorize with your JWT token and call:

POST /risk/analyze

This scores every log entry and populates the dashboard with real risk data.


Key Features Walkthrough

FeatureWhere to find itSOC Dashboard (risk distribution, trends, alerts)/dashboardEmployee list with search/filter/employeesExplainable AI reasons + MITRE mapping + Threat TimelineEmployee profile pageRisk-Based Access Control simulationEmployee profile page → "Run Access Control Check"Face Verification (Critical risk only)Triggered from employee profile, or /face-verify/:employee_idQuantum-Safe Credential Protection demo/quantum-safePDF Incident Report generationEmployee profile page → "Generate Incident Report"


Security Notes


Passwords are hashed with bcrypt — never stored in plain text.
JWT tokens expire automatically (default: 60 minutes).
All employee and face data in this repository is synthetic — no real individuals are represented.
Quantum-safe encryption uses real post-quantum cryptography (Kyber512 via Open Quantum Safe) when available, and clearly labels itself as a simulation when it falls back (this is expected on most local/free-tier environments due to native build requirements).



 Key Differentiators


Explainable, not a black box — every score comes with plain-English reasons and MITRE ATT&CK mapping.
Risk-adaptive, not blanket surveillance — biometric verification triggers only at Critical risk.
Forward-looking security — includes a quantum-safe credential protection module alongside today's controls.

Team

Team SriVerse - B S Bhargavi


License

This project was built for the Finspark Hackathon 2026 as a prototype/MVP and is provided as-is for demonstration purposes.
