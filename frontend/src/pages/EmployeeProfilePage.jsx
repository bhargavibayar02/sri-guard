// EmployeeProfilePage.jsx
// Detailed view of a single employee -- now fully wired with:
// Threat Timeline, Explainable AI reasons, MITRE mapping,
// Risk-Based Access Control simulation, Face Verification trigger,
// and Incident Report generation.

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axiosClient from "../api/axiosClient";
import RiskBadge from "../components/RiskBadge";
import ThreatTimeline from "../components/ThreatTimeline";
import MitreBadge from "../components/MitreBadge";

export default function EmployeeProfilePage() {
  const { employee_id } = useParams();
  const navigate = useNavigate();

  const [employee, setEmployee] = useState(null);
  const [worstLog, setWorstLog] = useState(null);
  const [error, setError] = useState("");
  const [accessResult, setAccessResult] = useState(null);
  const [incident, setIncident] = useState(null);
  const [loadingAccess, setLoadingAccess] = useState(false);
  const [loadingIncident, setLoadingIncident] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const empRes = await axiosClient.get(`/employees/${employee_id}`);
        setEmployee(empRes.data);

        const logsRes = await axiosClient.get(`/logs/${employee_id}`);
        // Find the highest-risk log entry for this employee
        const sorted = [...logsRes.data].sort(
          (a, b) => (b.risk_score || 0) - (a.risk_score || 0)
        );
        setWorstLog(sorted[0] || null);
      } catch (err) {
        setError("Employee not found.");
      }
    };
    fetchData();
  }, [employee_id]);

  const handleRunAccessControl = async () => {
    setLoadingAccess(true);
    try {
      const res = await axiosClient.post(`/access/simulate/${employee_id}`);
      setAccessResult(res.data);
    } catch (err) {
      console.error("Access control simulation failed", err);
    } finally {
      setLoadingAccess(false);
    }
  };

  const handleGenerateIncident = async () => {
    setLoadingIncident(true);
    try {
      const faceResult = employee.risk_score >= 90
        ? "Verification pending — see Face Verify page"
        : "Not Performed";
      const res = await axiosClient.post(
        `/incident/generate/${employee_id}`,
        null,
        { params: { face_verification_result: faceResult } }
      );
      setIncident(res.data);
    } catch (err) {
      console.error("Incident generation failed", err);
    } finally {
      setLoadingIncident(false);
    }
  };

  const handleDownloadPdf = () => {
    if (!incident) return;
    const token = localStorage.getItem("token");
    const apiUrl = import.meta.env.VITE_API_URL;
    // Open in a new tab with the token as a query param workaround isn't ideal for
    // production, but for this MVP we fetch it via axios and trigger a blob download.
    axiosClient
      .get(`/incident/${incident._id}/pdf`, { responseType: "blob" })
      .then((res) => {
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `Sri-Guard_Incident_${employee_id}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      })
      .catch((err) => console.error("PDF download failed", err));
  };

  if (error) {
    return (
      <div className="p-6">
        <p className="text-risk-critical">{error}</p>
        <button onClick={() => navigate(-1)} className="text-accent-500 mt-2">
          ← Go Back
        </button>
      </div>
    );
  }

  if (!employee) {
    return <p className="text-gray-400 p-6">Loading profile...</p>;
  }

  const isCritical = (employee.risk_score || 0) >= 90;

  return (
    <div className="p-6 space-y-6">
      <button onClick={() => navigate(-1)} className="text-accent-500 text-sm">
        ← Back to Employees
      </button>

      {/* --- Profile Header --- */}
      <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 fade-in">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-2xl font-bold text-white">{employee.name}</h2>
            <p className="text-gray-400">{employee.employee_id}</p>
          </div>
          <RiskBadge level={employee.risk_level || "Safe"} />
        </div>

        <div className="grid grid-cols-2 gap-4 mt-6 text-sm">
          <div>
            <p className="text-gray-500">Department</p>
            <p className="text-white">{employee.department}</p>
          </div>
          <div>
            <p className="text-gray-500">Role</p>
            <p className="text-white">{employee.role}</p>
          </div>
          <div>
            <p className="text-gray-500">Normal Working Hours</p>
            <p className="text-white">{employee.normal_working_hours}</p>
          </div>
          <div>
            <p className="text-gray-500">Risk Score</p>
            <p className="text-white">{employee.risk_score ?? 0} / 100</p>
          </div>
        </div>
      </div>

      {/* --- Critical Risk Banner --- */}
      {isCritical && (
        <div className="bg-risk-critical/10 border border-risk-critical/40 rounded-xl p-5 flex items-center justify-between fade-in">
          <div>
            <p className="text-risk-critical font-semibold">⚠️ Critical Risk — Identity Verification Required</p>
            <p className="text-sm text-gray-400 mt-1">
              This employee's behavior triggered a critical risk event.
            </p>
          </div>
          <button
            onClick={() => navigate(`/face-verify/${employee_id}`)}
            className="bg-risk-critical hover:opacity-90 text-white px-4 py-2 rounded-lg text-sm font-semibold whitespace-nowrap"
          >
             Verify Identity
          </button>
        </div>
      )}

      {/* --- Explainable AI Reasons + MITRE Mapping --- */}
      {worstLog && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 fade-in">
            <p className="text-sm text-gray-400 mb-3">Why This Was Flagged (Explainable AI)</p>
            {worstLog.risk_reasons && worstLog.risk_reasons.length > 0 ? (
              <ul className="space-y-2">
                {worstLog.risk_reasons.map((reason, i) => (
                  <li key={i} className="text-sm text-gray-300 flex gap-2">
                    <span className="text-risk-high">•</span> {reason}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-sm">No specific risk factors identified.</p>
            )}
          </div>

          <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 fade-in">
            <p className="text-sm text-gray-400 mb-3">MITRE ATT&CK Mapping</p>
            {worstLog.mitre_tags && worstLog.mitre_tags.length > 0 ? (
              <div>
                {worstLog.mitre_tags.map((tag, i) => (
                  <MitreBadge key={i} technique={tag} />
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No MITRE techniques matched.</p>
            )}
          </div>
        </div>
      )}

      {/* --- Threat Timeline --- */}
      {worstLog && (
        <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 fade-in">
          <p className="text-sm text-gray-400 mb-4">Threat Timeline</p>
          <ThreatTimeline timeline={worstLog.timeline || generateClientTimeline(worstLog)} />
        </div>
      )}

      {/* --- Risk-Based Access Control --- */}
      <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 fade-in space-y-4">
        <div className="flex justify-between items-center">
          <p className="text-sm text-gray-400">Risk-Based Access Control</p>
          <button
            onClick={handleRunAccessControl}
            disabled={loadingAccess}
            className="bg-accent-600 hover:bg-accent-500 text-white px-4 py-2 rounded-lg text-sm font-semibold disabled:opacity-50"
          >
            {loadingAccess ? "Simulating..." : "Run Access Control Check"}
          </button>
        </div>

        {accessResult && (
          <div className="text-sm space-y-2 bg-navy-900 rounded-lg p-4">
            <p className="text-gray-300">{accessResult.message}</p>
            <div className="grid grid-cols-2 gap-2 mt-2">
              <p className="text-gray-500">Account Locked: <span className="text-white">{String(accessResult.actions.account_locked)}</span></p>
              <p className="text-gray-500">MFA Forced: <span className="text-white">{String(accessResult.actions.mfa_forced)}</span></p>
              <p className="text-gray-500">SOC Notified: <span className="text-white">{String(accessResult.actions.soc_notified)}</span></p>
              <p className="text-gray-500">Incident Generated: <span className="text-white">{String(accessResult.actions.incident_generated)}</span></p>
            </div>
          </div>
        )}
      </div>

      {/* --- Incident Report --- */}
      <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 fade-in space-y-4">
        <div className="flex justify-between items-center">
          <p className="text-sm text-gray-400">Incident Report</p>
          <button
            onClick={handleGenerateIncident}
            disabled={loadingIncident}
            className="bg-accent-600 hover:bg-accent-500 text-white px-4 py-2 rounded-lg text-sm font-semibold disabled:opacity-50"
          >
            {loadingIncident ? "Generating..." : "Generate Incident Report"}
          </button>
        </div>

        {incident && (
          <div className="bg-navy-900 rounded-lg p-4 flex items-center justify-between">
            <p className="text-sm text-gray-300">
              Incident generated for {incident.employee_id} — Risk {incident.risk_score}/100
            </p>
            <button
              onClick={handleDownloadPdf}
              className="bg-navy-700 hover:bg-navy-600 text-white px-4 py-2 rounded-lg text-sm"
            >
               Download PDF
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// Fallback: builds a simple client-side timeline if the log doesn't
// already include one from the backend (kept lightweight, mirrors
// the backend's threat_timeline.py logic in simplified form).
function generateClientTimeline(log) {
  const events = [];
  const loginTime = log.login_time ? log.login_time.split(" ")[1]?.slice(0, 5) : "??:??";
  events.push(`${loginTime} — Login from ${log.device}`);
  if (log.failed_logins > 0) events.push(`+2min — ${log.failed_logins} failed login attempt(s)`);
  if (log.database_access && log.database_access !== "None") events.push(`+4min — Accessed ${log.database_access}`);
  if (log.files_downloaded > 0) events.push(`+6min — Downloaded ${log.files_downloaded} file(s)`);
  if (log.usb_connected) events.push(`+7min — USB storage device connected`);
  if (log.admin_access) events.push(`+8min — Administrator-level access used`);
  if (log.risk_score > 70) events.push(`+9min — ⚠️ Risk Alert Generated (Score: ${log.risk_score})`);
  return events;
}