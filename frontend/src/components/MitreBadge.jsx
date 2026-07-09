// MitreBadge.jsx
// A small tag showing a MITRE ATT&CK technique.

export default function MitreBadge({ technique }) {
  return (
    <span className="inline-block px-3 py-1 mb-2 mr-2 rounded-lg text-xs bg-navy-700 border border-navy-600 text-gray-300">
      {technique}
    </span>
  );
}