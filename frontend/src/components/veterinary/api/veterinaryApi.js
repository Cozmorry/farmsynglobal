// src/components/veterinary/api/veterinaryApi.js
import axios from "axios";

// ============================
// Recommendations
// ============================
export const getVeterinaryRecommendations = async () => {
  const res = await axios.get("/api/veterinary/recommendations");
  return res.data;
};

export const createVeterinaryRecommendation = async (data) => {
  const res = await axios.post("/api/veterinary/recommendations", data);
  return res.data;
};

export const updateVeterinaryRecommendation = async (id, data) => {
  const res = await axios.put(`/api/veterinary/recommendations/${id}`, data);
  return res.data;
};

export const deleteVeterinaryRecommendation = async (id) => {
  const res = await axios.delete(`/api/veterinary/recommendations/${id}`);
  return res.data;
};

// ============================
// File uploads
// ============================
export const uploadVeterinaryRecommendationFile = async (formData) => {
  const res = await axios.post("/api/veterinary/recommendation-files", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

export const getVeterinaryRecommendationUploads = async ({ recommendation_id }) => {
  const res = await axios.get(`/api/veterinary/recommendation-files?recommendation_id=${recommendation_id}`);
  return res.data;
};

export const uploadVeterinaryHealthFile = async (formData) => {
  const res = await axios.post("/api/veterinary/health-files", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

export const getVeterinaryHealthUploads = async ({ health_id }) => {
  const res = await axios.get(`/api/veterinary/health-files?health_id=${health_id}`);
  return res.data;
};

