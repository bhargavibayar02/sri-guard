// AlertsTable.jsx
// Shows the "Recent Alerts" list on the dashboard.

import RiskBadge from "./RiskBadge";
import { getRiskLevel } from "../utils/riskColors";

export default function AlertsTable({ alerts }) {
  return (
    <div className="bg-navy-800 border border-navy-700 rounded-xl p-5 fade-in">
      <p className="text-sm text-gray-400 mb-3">Recent Alerts</p>
      {alerts.length === 0 ? (
        <p className="text-gray-500 text-sm">No alerts yet.</p>
      ) : (
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b border-navy-700">
              <th className="pb-2">Employee ID</th>
              <th className="pb-2">Time</th>
              <th className="pb-2">Risk</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((a, i) => (
              <tr key={i} className="border-b border-navy-700/50">
                <td className="py-2 text-white">{a.employee_id}</td>
                <td className="py-2 text-gray-400">{a.login_time}</td>
                <td className="py-2">
                  <RiskBadge level={getRiskLevel(a.risk_score)} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}