// DepartmentRiskChart.jsx
// Bar chart showing average risk score per department.
// Pulls live data from GET /dashboard/department-risk

import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function DepartmentRiskChart({ departments }) {
  const chartData = {
    labels: departments.map((d) => d.department),
    datasets: [
      {
        label: "Average Risk Score",
        data: departments.map((d) => d.avg_risk),
        backgroundColor: "#2563eb",
        borderRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { labels: { color: "#94a3b8" } },
    },
    scales: {
      x: { ticks: { color: "#64748b" }, grid: { color: "#182a4a" } },
      y: { ticks: { color: "#64748b" }, grid: { color: "#182a4a" } },
    },
  };

  return (
    <div className="bg-navy-800 border border-navy-700 rounded-xl p-5 fade-in">
      <p className="text-sm text-gray-400 mb-3">Department Wise Risk</p>
      {departments.length === 0 ? (
        <p className="text-gray-500 text-sm">No employee data yet.</p>
      ) : (
        <Bar data={chartData} options={options} />
      )}
    </div>
  );
}