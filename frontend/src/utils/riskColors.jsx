// riskColors.js
// Small helper: given a risk score or risk level string,
// returns the right Tailwind color classes for badges/charts.

export function getRiskLevel(score) {
  if (score <= 40) return "Safe";
  if (score <= 70) return "Medium";
  if (score <= 90) return "High";
  return "Critical";
}

export function getRiskColorClasses(level) {
  switch (level) {
    case "Safe":
      return "bg-risk-safe/20 text-risk-safe border border-risk-safe/40";
    case "Medium":
      return "bg-risk-medium/20 text-risk-medium border border-risk-medium/40";
    case "High":
      return "bg-risk-high/20 text-risk-high border border-risk-high/40";
    case "Critical":
      return "bg-risk-critical/20 text-risk-critical border border-risk-critical/40";
    default:
      return "bg-gray-500/20 text-gray-400 border border-gray-500/40";
  }
}

export function getRiskHexColor(level) {
  switch (level) {
    case "Safe": return "#22c55e";
    case "Medium": return "#eab308";
    case "High": return "#f97316";
    case "Critical": return "#ef4444";
    default: return "#94a3b8";
  }
}