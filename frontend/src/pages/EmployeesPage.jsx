// EmployeesPage.jsx
// Employee list with search + department filter.

import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import EmployeeTable from "../components/EmployeeTable";

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("");

  const fetchEmployees = async () => {
    try {
      const params = {};
      if (search) params.search = search;
      if (department) params.department = department;
      const res = await axiosClient.get("/employees/", { params });
      setEmployees(res.data);
    } catch (err) {
      console.error("Failed to load employees", err);
    }
  };

  useEffect(() => {
    fetchEmployees();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search, department]);

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-bold text-white">Employee Management</h2>

      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Search by name or ID..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 px-4 py-2 rounded-lg bg-navy-800 border border-navy-700 text-white focus:outline-none focus:border-accent-500"
        />
        <select
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
          className="px-4 py-2 rounded-lg bg-navy-800 border border-navy-700 text-white focus:outline-none focus:border-accent-500"
        >
          <option value="">All Departments</option>
          <option value="Finance">Finance</option>
          <option value="IT">IT</option>
          <option value="HR">HR</option>
          <option value="Operations">Operations</option>
        </select>
      </div>

      <EmployeeTable employees={employees} />
    </div>
  );
}