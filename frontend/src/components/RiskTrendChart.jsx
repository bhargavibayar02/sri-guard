// RiskTrendChart.jsx
// Line graph showing average risk score over time (placeholder data
// until Phase 5's ML engine produces real historical scores).

import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

export default function RiskTrendChart({ labels, data }) {
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Average Risk Score",
        data: data,
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59, 130, 246, 0.15)",
        tension: 0.35,
        fill: true,
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
      <p className="text-sm text-gray-400 mb-3">Risk Trend (Last 7 Days)</p>
      <Line data={chartData} options={options} />
    </div>
  );
}