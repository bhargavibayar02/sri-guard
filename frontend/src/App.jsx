// App.jsx
// Sets up all page routes.

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import DashboardLayout from "./components/DashboardLayout";

import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import EmployeesPage from "./pages/EmployeesPage";
import EmployeeProfilePage from "./pages/EmployeeProfilePage";
import LogsPage from "./pages/LogsPage";
import FaceVerifyPage from "./pages/FaceVerifyPage";
import QuantumSafePage from "./pages/QuantumSafePage";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route
            path="/"
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="employees" element={<EmployeesPage />} />
            <Route path="employees/:employee_id" element={<EmployeeProfilePage />} />
            <Route path="logs" element={<LogsPage />} />
            <Route path="face-verify/:employee_id" element={<FaceVerifyPage />} />
            <Route path="quantum-safe" element={<QuantumSafePage />} />
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}