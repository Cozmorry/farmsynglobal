// src/core/config/env.js
// Use Vite env variables in production, empty string in dev (proxy handles requests)
export const API_BASE_URL = import.meta.env.PROD
  ? import.meta.env.VITE_API_BASE_URL || "https://api.farmsynglobal.online"
  : ""; // empty string → Vite proxy will handle /api requests in dev
