// axiosClient.js
// A single configured Axios instance used by the WHOLE app.
// It automatically attaches the JWT token to every request,
// so we never have to repeat that logic in each page.

import axios from "axios";

const axiosClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// This runs BEFORE every request is sent
axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// This runs AFTER every response -- if the token is invalid/expired,
// automatically log the user out and send them back to login
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default axiosClient;