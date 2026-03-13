//src/dashboard.js

import { API_BASE_URL } from "./core/config/env";

export async function getDashboardSummary(token) {
  const farmId = 1;

  const response = await fetch(
    `${API_BASE_URL}/dashboard/summary/${farmId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) throw new Error("Failed to fetch dashboard summary");

  return response.json();
}
