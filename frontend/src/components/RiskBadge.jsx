// RiskBadge.jsx
// A small colored pill showing a risk level, e.g. "High" in orange.

import { getRiskColorClasses } from "../utils/riskColors";

export default function RiskBadge({ level }) {
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getRiskColorClasses(level)}`}>
      {level}
    </span>
  );
}