// LogsPage.jsx
// Shows all activity logs in a table.

import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import RiskBadge from "../components/RiskBadge";
import { getRiskLevel } from "../utils/riskColors";

export default function LogsPage() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await axiosClient.get("/logs/");
        setLogs(res.data);
      } catch (err) {
        console.error("Failed to load logs", err);
      }
    };
    fetchLogs();
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-bold text-white">Activity Logs</h2>

      <div className="bg-navy-800 border border-navy-700 rounded-xl p-5 overflow-x-auto fade-in">
        {logs.length === 0 ? (
          <p className="text-gray-500 text-sm">No logs found. Load the dataset in Phase 5.</p>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-500 border-b border-navy-700">
                <th className="pb-2">Employee</th>
                <th className="pb-2">Login Time</th>
                <th className="pb-2">Device</th>
                <th className="pb-2">IP</th>
                <th className="pb-2">Failed Logins</th>
                <th className="pb-2">Files DL</th>
                <th className="pb-2">USB</th>
                <th className="pb-2">DB Access</th>
                <th className="pb-2">Risk</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, i) => (
                <tr key={i} className="border-b border-navy-700/50">
                  <td className="py-2 text-white">{log.employee_id}</td>
                  <td className="py-2 text-gray-400">{log.login_time}</td>
                  <td className="py-2 text-gray-400">{log.device}</td>
                  <td className="py-2 text-gray-400">{log.ip_address}</td>
                  <td className="py-2 text-gray-400">{log.failed_logins}</td>
                  <td className="py-2 text-gray-400">{log.files_downloaded}</td>
                  <td className="py-2 text-gray-400">{log.usb_connected ? "Yes" : "No"}</td>
                  <td className="py-2 text-gray-400">{log.database_access}</td>
                  <td className="py-2">
                    <RiskBadge level={getRiskLevel(log.risk_score || 0)} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}