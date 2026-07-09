// Navbar.jsx
// Top bar shown on every page after login -- shows app name and logout button.

import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="h-16 bg-navy-900 border-b border-navy-700 flex items-center justify-between px-6">
      <h1 className="text-lg font-bold text-white tracking-wide">
         Sri-Guard <span className="text-accent-500">SOC Console</span>
      </h1>
      <button
        onClick={handleLogout}
        className="text-sm px-4 py-2 rounded-lg bg-navy-800 hover:bg-navy-700 text-gray-300 transition"
      >
        Logout
      </button>
    </div>
  );
}