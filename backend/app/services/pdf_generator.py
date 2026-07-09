# pdf_generator.py
# Builds a professional PDF Incident Report using ReportLab.
# Includes: employee info, risk score, explainable AI reasons,
# threat timeline, MITRE mapping, face verification result,
# recommended action, and timestamp.

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "generated_reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_incident_pdf(incident: dict) -> str:
    """
    Generates a PDF file from an incident dict and returns the file path.
    """
    filename = f"incident_{incident['employee_id']}_{int(datetime.utcnow().timestamp())}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], textColor=colors.HexColor("#0a1428"), fontSize=20
    )
    heading_style = ParagraphStyle(
        "HeadingStyle", parent=styles["Heading2"], textColor=colors.HexColor("#2563eb"), spaceBefore=14
    )
    body_style = styles["BodyText"]

    elements = []

    # --- Title ---
    elements.append(Paragraph("🛡️ Sri-Guard Incident Report", title_style))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(f"Generated: {incident['created_at']}", body_style))
    elements.append(Spacer(1, 0.5*cm))

    # --- Employee Info Table ---
    elements.append(Paragraph("Employee Information", heading_style))
    info_table_data = [
        ["Employee ID", incident["employee_id"]],
        ["Department", incident["department"]],
        ["Risk Score", f"{incident['risk_score']} / 100"],
        ["Recommended Action", incident["recommended_action"]],
    ]
    info_table = Table(info_table_data, colWidths=[5*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e2e8f0")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)

    # --- Reasons (Explainable AI) ---
    elements.append(Paragraph("Why This Was Flagged (Explainable AI)", heading_style))
    if incident["reasons"]:
        for reason in incident["reasons"]:
            elements.append(Paragraph(f"• {reason}", body_style))
    else:
        elements.append(Paragraph("No specific risk factors identified.", body_style))

    # --- Threat Timeline ---
    elements.append(Paragraph("Threat Timeline", heading_style))
    if incident["timeline"]:
        for event in incident["timeline"]:
            elements.append(Paragraph(event, body_style))
    else:
        elements.append(Paragraph("No timeline data available.", body_style))

    # --- MITRE ATT&CK Mapping ---
    elements.append(Paragraph("MITRE ATT&CK Mapping", heading_style))
    if incident["mitre_mapping"]:
        for tag in incident["mitre_mapping"]:
            elements.append(Paragraph(f"• {tag}", body_style))
    else:
        elements.append(Paragraph("No MITRE techniques matched.", body_style))

    # --- Face Verification Result ---
    elements.append(Paragraph("Face Verification Result", heading_style))
    elements.append(Paragraph(incident.get("face_verification_result", "Not Performed"), body_style))

    doc.build(elements)
    return filepath