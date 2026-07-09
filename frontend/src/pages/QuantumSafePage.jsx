// QuantumSafePage.jsx
// A simple demo page showing the Quantum-Safe Credential Protection
// module in action -- lets the SOC analyst type a credential and see
// it encrypted (real or simulated, clearly labeled either way).

import { useState, useEffect } from "react";
import axiosClient from "../api/axiosClient";

export default function QuantumSafePage() {
  const [status, setStatus] = useState(null);
  const [credential, setCredential] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await axiosClient.get("/quantum/status");
        setStatus(res.data);
      } catch (err) {
        console.error("Failed to load quantum status", err);
      }
    };
    fetchStatus();
  }, []);

  const handleEncrypt = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axiosClient.post("/quantum/encrypt-demo", { credential });
      setResult(res.data);
    } catch (err) {
      setResult({ note: "Encryption demo failed." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl space-y-6">
      <h2 className="text-xl font-bold text-white"> Quantum-Safe Credential Protection</h2>

      {status && (
        <div
          className={`p-4 rounded-lg text-sm border ${
            status.oqs_available
              ? "bg-risk-safe/10 border-risk-safe/40 text-risk-safe"
              : "bg-risk-medium/10 border-risk-medium/40 text-risk-medium"
          }`}
        >
          <p className="font-semibold">
            Status: {status.oqs_available ? "Real Post-Quantum Encryption Active" : "Simulation Mode (MVP Demo)"}
          </p>
          <p className="text-xs text-gray-400 mt-1">{status.message}</p>
        </div>
      )}

      <form onSubmit={handleEncrypt} className="bg-navy-800 border border-navy-700 rounded-xl p-6 space-y-4">
        <label className="text-sm text-gray-400">Admin Credential (demo text)</label>
        <input
          type="text"
          value={credential}
          onChange={(e) => setCredential(e.target.value)}
          placeholder="e.g. admin_secret_password_123"
          className="w-full px-4 py-2 rounded-lg bg-navy-900 border border-navy-700 text-white focus:outline-none focus:border-accent-500"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent-600 hover:bg-accent-500 text-white py-2 rounded-lg font-semibold transition disabled:opacity-50"
        >
          {loading ? "Encrypting..." : "Run Quantum-Safe Encryption Demo"}
        </button>
      </form>

      {result && (
        <div className="bg-navy-800 border border-navy-700 rounded-xl p-6 space-y-2 text-sm fade-in">
          <p className="text-gray-400">Mode: <span className="text-white">{result.mode}</span></p>
          <p className="text-gray-400">Algorithm: <span className="text-white">{result.algorithm}</span></p>
          <p className="text-gray-400 break-all">
            Encrypted Output: <span className="text-accent-500">{result.encrypted_data}</span>
          </p>
          <p className="text-xs text-gray-500 mt-2">{result.note}</p>
        </div>
      )}
    </div>
  );
}