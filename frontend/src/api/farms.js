//src/api/farms.js
import api from "./axios";

export async function getFarms() {
  try {
    const res = await api.get("/farms");
    return res.data;
  } catch (err) {
    throw new Error(err.response?.data?.detail || "Failed to fetch farms");
  }
}

export async function createFarm(farm) {
  try {
    const res = await api.post("/farms", farm);
    return res.data;
  } catch (err) {
    throw new Error(err.response?.data?.detail || "Failed to create farm");
  }
}

