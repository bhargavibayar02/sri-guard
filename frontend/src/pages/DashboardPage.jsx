// DashboardPage.jsx
// Main SOC dashboard -- pulls summary stats, department risk, and recent alerts.

import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import StatCard from "../components/StatCard";
import RiskTrendChart from "../components/RiskTrendChart";
import DepartmentRiskChart from "../components/DepartmentRiskChart";
import AlertsTable from "../components/AlertsTable";

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [departments, setDepartments] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryRes, deptRes, alertsRes] = await Promise.all([
          axiosClient.get("/dashboard/summary"),
          axiosClient.get("/dashboard/department-risk"),
          axiosClient.get("/dashboard/recent-alerts"),
        ]);
        setSummary(summaryRes.data);
        setDepartments(deptRes.data);
        setAlerts(alertsRes.data);
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      }
    };
    fetchData();
  }, []);

  if (!summary) {
    return <p className="text-gray-400 p-6">Loading dashboard...</p>;
  }

  // Placeholder trend data until Phase 5 ML produces real historical scores
  const trendLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Today"];
  const trendData = [20, 25, 22, 30, 28, 35, summary.critical * 10 || 20];

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-bold text-white">Dashboard Overview</h2>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <StatCard title="Total Employees" value={summary.total_employees} />
        <StatCard title="Safe" value={summary.safe} colorClass="text-risk-safe" />
        <StatCard title="Medium Risk" value={summary.medium} colorClass="text-risk-medium" />
        <StatCard title="High Risk" value={summary.high} colorClass="text-risk-high" />
        <StatCard title="Critical Alerts" value={summary.critical_alerts} colorClass="text-risk-critical" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <RiskTrendChart labels={trendLabels} data={trendData} />
        <DepartmentRiskChart departments={departments} />
      </div>

      <AlertsTable alerts={alerts} />
    </div>
  );
}