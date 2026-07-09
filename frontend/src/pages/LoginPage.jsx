// LoginPage.jsx
// The SOC Analyst login screen -- calls POST /auth/login

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosClient from "../api/axiosClient";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await axiosClient.post("/auth/login", { username, password });
      login(res.data.access_token, res.data.role);
      navigate("/dashboard");
    } catch (err) {
      setError("Invalid username or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-navy-950">
      <form
        onSubmit={handleSubmit}
        className="bg-navy-800 border border-navy-700 rounded-2xl p-8 w-96 fade-in"
      >
        <h1 className="text-2xl font-bold text-white mb-1">Sri-Guard</h1>
        <p className="text-gray-400 text-sm mb-6">SOC Analyst Login</p>

        {error && (
          <div className="bg-risk-critical/10 border border-risk-critical/40 text-risk-critical text-sm rounded-lg p-3 mb-4">
            {error}
          </div>
        )}

        <label className="text-sm text-gray-400">Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full mt-1 mb-4 px-4 py-2 rounded-lg bg-navy-900 border border-navy-700 text-white focus:outline-none focus:border-accent-500"
          placeholder="admin"
          required
        />

        <label className="text-sm text-gray-400">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mt-1 mb-6 px-4 py-2 rounded-lg bg-navy-900 border border-navy-700 text-white focus:outline-none focus:border-accent-500"
          placeholder="••••••••"
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent-600 hover:bg-accent-500 text-white py-2 rounded-lg font-semibold transition disabled:opacity-50"
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}