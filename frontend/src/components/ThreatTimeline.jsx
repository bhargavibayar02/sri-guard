// ThreatTimeline.jsx
// Displays a vertical timeline of events, e.g. "09:00 Login", "09:07 Finance DB accessed"

export default function ThreatTimeline({ timeline }) {
  if (!timeline || timeline.length === 0) {
    return <p className="text-gray-500 text-sm">No timeline data available.</p>;
  }

  return (
    <div className="space-y-3">
      {timeline.map((event, i) => (
        <div key={i} className="flex items-start gap-3">
          <div className="w-2 h-2 rounded-full bg-accent-500 mt-1.5 flex-shrink-0" />
          <p className="text-sm text-gray-300">{event}</p>
        </div>
      ))}
    </div>
  );
}