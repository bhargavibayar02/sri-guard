// StatCard.jsx
// The small boxes on the dashboard showing "Total Employees", "Critical Alerts", etc.

export default function StatCard({ title, value, colorClass = "text-white" }) {
  return (
    <div className="bg-navy-800 border border-navy-700 rounded-xl p-5 fade-in">
      <p className="text-sm text-gray-400 mb-1">{title}</p>
      <p className={`text-3xl font-bold ${colorClass}`}>{value}</p>
    </div>
  );
}