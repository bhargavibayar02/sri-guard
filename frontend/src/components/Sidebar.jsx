// Sidebar.jsx
// Left-side navigation menu.

import { NavLink } from "react-router-dom";

const links = [
  { to: "/dashboard", label: "Dashboard", icon: "" },
  { to: "/employees", label: "Employees", icon: "" },
  { to: "/logs", label: "Activity Logs", icon: "" },
  { to: "/quantum-safe", label: "Quantum-Safe Demo", icon: "" },
];

export default function Sidebar() {
  return (
    <div className="w-56 bg-navy-900 border-r border-navy-700 h-full py-6 px-3">
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) =>
            `flex items-center gap-3 px-4 py-3 rounded-lg mb-1 text-sm transition ${
              isActive
                ? "bg-accent-600 text-white"
                : "text-gray-400 hover:bg-navy-800 hover:text-white"
            }`
          }
        >
          <span>{link.icon}</span>
          {link.label}
        </NavLink>
      ))}
    </div>
  );
}