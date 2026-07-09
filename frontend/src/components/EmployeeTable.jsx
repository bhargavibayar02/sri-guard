// EmployeeTable.jsx
// Table listing employees with search/filter, used on the Employees page.

import { useNavigate } from "react-router-dom";
import RiskBadge from "./RiskBadge";

export default function EmployeeTable({ employees }) {
  const navigate = useNavigate();

  return (
    <div className="bg-navy-800 border border-navy-700 rounded-xl p-5 fade-in overflow-x-auto">
      {employees.length === 0 ? (
        <p className="text-gray-500 text-sm">No employees found.</p>
      ) : (
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b border-navy-700">
              <th className="pb-2">ID</th>
              <th className="pb-2">Name</th>
              <th className="pb-2">Department</th>
              <th className="pb-2">Role</th>
              <th className="pb-2">Risk</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((emp) => (
              <tr
                key={emp.employee_id}
                onClick={() => navigate(`/employees/${emp.employee_id}`)}
                className="border-b border-navy-700/50 hover:bg-navy-700/40 cursor-pointer transition"
              >
                <td className="py-3 text-white">{emp.employee_id}</td>
                <td className="py-3 text-white">{emp.name}</td>
                <td className="py-3 text-gray-400">{emp.department}</td>
                <td className="py-3 text-gray-400">{emp.role}</td>
                <td className="py-3">
                  <RiskBadge level={emp.risk_level || "Safe"} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}