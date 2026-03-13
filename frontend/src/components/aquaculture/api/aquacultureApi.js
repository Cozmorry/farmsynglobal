//src/components/aquaculture/api/aquacultureApi.js
import axios from "axios";

const API_URL = "/api/aquaculture"; // Adjust base URL if different

// =======================
// PONDS
// =======================
export const getPonds = async () => {
  return axios.get(`${API_URL}/ponds`);
};

export const createPond = async (data) => {
  return axios.post(`${API_URL}/ponds`, data);
};

export const deletePond = async (id) => {
  return axios.delete(`${API_URL}/ponds/${id}`);
};


// =======================
// WATER QUALITY
// =======================
export const getWaterRecords = async ({ pond_id }) => {
  return axios.get(`${API_URL}/water_quality`, { params: { pond_id } });
};

export const createWaterRecord = async (data) => {
  return axios.post(`${API_URL}/water_quality`, data);
};

export const deleteWaterRecord = async (id) => {
  return axios.delete(`${API_URL}/water_quality/${id}`);
};

// =======================
// HARVESTS
// =======================
export const getHarvests = async ({ pond_id }) => {
  return axios.get(`${API_URL}/harvest`, { params: { pond_id } });
};

export const createHarvest = async (data) => {
  return axios.post(`${API_URL}/harvest`, data);
};

export const deleteHarvest = async (id) => {
  return axios.delete(`${API_URL}/harvest/${id}`);
};

// =======================
// ACTIVITIES
// =======================
export const getActivities = async ({ pond_id }) => {
  return axios.get(`${API_URL}/activity`, { params: { pond_id } });
};

export const createActivity = async (data) => {
  return axios.post(`${API_URL}/activity`, data);
};

export const deleteActivity = async (id) => {
  return axios.delete(`${API_URL}/activity/${id}`);
};

// =======================
// HEALTH
// =======================
export const getHealth = async ({ pond_id }) => {
  return axios.get(`${API_URL}/health`, { params: { pond_id } });
};

export const createHealth = async (data) => {
  return axios.post(`${API_URL}/health`, data);
};

export const deleteHealth = async (id) => {
  return axios.delete(`${API_URL}/health/${id}`);
};

// =======================
// VETERINARY RECOMMENDATIONS
// =======================
export const getRecommendations = async ({ health_id }) => {
  return axios.get(`${API_URL}/recommendation`, { params: { health_id } });
};

export const createRecommendation = async (data) => {
  return axios.post(`${API_URL}/recommendation`, data);
};

export const deleteRecommendation = async (id) => {
  return axios.delete(`${API_URL}/recommendation/${id}`);
};

// =======================
// PRODUCTION
// =======================
export const getProductions = async ({ pond_id }) => {
  return axios.get(`${API_URL}/production`, { params: { pond_id } });
};

export const createProduction = async (data) => {
  return axios.post(`${API_URL}/production`, data);
};

export const deleteProduction = async (id) => {
  return axios.delete(`${API_URL}/production/${id}`);
};


// =======================
// FEEDINGS
// =======================
export const getFeedings = async ({ pond_id }) => {
  return axios.get(`${API_URL}/feedings`, { params: { pond_id } });
};

export const createFeeding = async (data) => {
  return axios.post(`${API_URL}/feedings`, data);
};

export const deleteFeeding = async (id) => {
  return axios.delete(`${API_URL}/feedings/${id}`);
};
