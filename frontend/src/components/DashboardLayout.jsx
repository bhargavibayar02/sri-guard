// DashboardLayout.jsx
// Wraps all logged-in pages with the Navbar + Sidebar.

import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

export default function DashboardLayout() {
  return (
    <div className="h-screen flex flex-col bg-navy-900">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <div className="flex-1 overflow-y-auto">
          <Outlet />
        </div>
      </div>
    </div>
  );
}