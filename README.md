# Sri-Guard

**Explainable AI-Powered Insider Threat Prevention Platform with Risk-Adaptive Access Control and Quantum-Safe Credential Protection**

Built for the **Finspark Hackathon 2026**

---

## Problem Statement

Insider threats — from employees, contractors, vendors, and admins — acting maliciously, negligently, or under compromise pose serious risk to banking security and data integrity. Sri-Guard was built to detect privileged access misuse before it becomes a breach.

### Focus Areas
- Insider Threat Detection
- Behaviour Analytics
- Privileged Access Management
- Risk-Based Authentication
- Quantum-Safe Security

---

##  What Sri-Guard Does

Unlike traditional insider-threat tools that output a single opaque risk score, Sri-Guard is built to be **explainable end-to-end**:

1. **Detects** misuse of privileged accounts and identifies insider threats in real time using AI-driven behavioural analysis (Isolation Forest anomaly detection).
2. **Explains** every flagged event in plain English (e.g. *"Login at unusual time," "USB device connected," "Accessed Finance DB"*) instead of a black-box score.
3. **Maps** each reason to real **MITRE ATT&CK** techniques, making alerts SOC-analyst ready out of the box.
4. **Reconstructs** a chronological **Threat Timeline** for every flagged session.
5. **Simulates Risk-Based Access Control** — locking the account, forcing MFA, and notifying the SOC team when risk crosses a critical threshold.
6. **Verifies identity** via webcam-based **Face Verification** (DeepFace), triggered *only* at Critical risk — never continuous surveillance.
7. **Generates a downloadable PDF Incident Report** containing the full investigation trail: risk score, reasons, timeline, MITRE mapping, and verification outcome.
8. **Demonstrates Quantum-Safe Credential Protection** — encrypting sensitive credentials using post-quantum cryptography (Kyber, NIST-standardized), with a clearly labeled simulation fallback where native quantum-safe libraries aren't available.

---



##  Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React, Tailwind CSS, Chart.js |
| **Backend** | FastAPI (Python) |
| **Database** | MongoDB (Atlas) |
| **Machine Learning** | Python, Pandas, Scikit-learn (Isolation Forest) |
| **Face Verification** | DeepFace, OpenCV |
| **Authentication** | JWT, bcrypt |
| **PDF Reports** | ReportLab |
| **Quantum-Safe Crypto** | Open Quantum Safe (liboqs) — with simulated fallback |
| **Deployment** | Vercel (frontend), Render (backend), MongoDB Atlas (database) |

---
---

## ⚙️ Prerequisites

- Python 3.11
- Node.js 18+
- MongoDB (local instance or MongoDB Atlas)
- A webcam (for the Face Verification demo)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/sri-guard.git
cd sri-guard
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=sriguard
JWT_SECRET=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

### 3. Generate the dataset

```bash
cd ../dataset
python generate_dataset.py
python generate_faces.py
cd ../backend
```

### 4. Seed the database and train the model

```bash
python seed/create_admin.py
python seed/seed_data.py
python seed/create_indexes.py
python app/ml/train_model.py
```

### 5. Run the backend

```bash
uvicorn app.main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### 6. Run the frontend

```bash
cd ../frontend
npm install
npm run dev
```

App available at: `http://localhost:5173`



---

##  Key Features Walkthrough

| Feature | Where to find it |
|---|---|
| SOC Dashboard (risk distribution, trends, alerts) | `/dashboard` |
| Employee list with search/filter | `/employees` |
| Explainable AI reasons + MITRE mapping + Threat Timeline | Employee profile page |
| Risk-Based Access Control simulation | Employee profile page → "Run Access Control Check" |
| Face Verification (Critical risk only) | Triggered from employee profile, or `/face-verify/:employee_id` |
| Quantum-Safe Credential Protection demo | `/quantum-safe` |
| PDF Incident Report generation | Employee profile page → "Generate Incident Report" |

---

##  Security Notes

- Passwords are hashed with bcrypt — never stored in plain text.
- JWT tokens expire automatically (default: 60 minutes).
- All employee and face data in this repository is **synthetic** — no real individuals are represented.
- Quantum-safe encryption uses real post-quantum cryptography (Kyber512 via Open Quantum Safe) when available, and clearly labels itself as a simulation when it falls back (this is expected on most local/free-tier environments due to native build requirements).

---

##  Key Differentiators

- **Explainable, not a black box** — every score comes with plain-English reasons and MITRE ATT&CK mapping.
- **Risk-adaptive, not blanket surveillance** — biometric verification triggers only at Critical risk.
- **Forward-looking security** — includes a quantum-safe credential protection module alongside today's controls.


##  Team

**Team SriVerse**
- B S Bhargavi

---

##  License

This project was built for the Finspark Hackathon 2026 as a prototype/MVP and is provided as-is for demonstration purposes.

### 7. Log in
Demo:
<img width="1920" height="1020" alt="Screenshot 2026-07-09 151526" src="https://github.com/user-attachments/assets/b696518e-7d3d-49b0-bee0-741adbbdb3ae" />
<img width="1920" height="1020" alt="Screenshot 2026-07-09 151615" src="https://github.com/user-attachments/assets/b922845c-16cd-4317-8fcc-728d0a0b855c" />


