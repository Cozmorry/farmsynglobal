// src/api/axios.js
import axios from "axios";
import { API_BASE_URL } from "../core/config/env";

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;

    const currentFarmId = localStorage.getItem("current_farm_id");
    if (currentFarmId) config.headers["X-Farm-ID"] = currentFarmId;

    const currentTenantId = localStorage.getItem("current_tenant_id");
    if (currentTenantId) config.headers["X-Tenant-ID"] = currentTenantId;

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;

    if (status === 401) {
      localStorage.clear();
      window.location.href = "/login";
    } else if (status === 403) {
      alert("You do not have permission to access this resource.");
    } else if (status === 429) {
      alert("Too many requests! Please try again later.");
    }

    console.error("API Error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;
