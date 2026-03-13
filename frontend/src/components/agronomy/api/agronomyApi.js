// src/components/agronomy/api/agronomyApi.js
import api from "../../../api/axios"; // Adjust path according to your project structure

const BASE = "/api/agronomy";

// Recommendations
export const getRecommendations = (params) => api.get(`${BASE}/recommendations/`, { params });
export const createRecommendation = (data) => api.post(`${BASE}/recommendations/`, data);
export const updateRecommendation = (id, data) => api.put(`${BASE}/recommendations/${id}/`, data);
export const deleteRecommendation = (id) => api.delete(`${BASE}/recommendations/${id}/`);

// Observations
export const getObservations = (params) => api.get(`${BASE}/observations/`, { params });
export const createObservation = (data) => api.post(`${BASE}/observations/`, data);
export const updateObservation = (id, data) => api.put(`${BASE}/observations/${id}/`, data);
export const deleteObservation = (id) => api.delete(`${BASE}/observations/${id}/`);

// Recommendation uploads
export const getRecommendationUploads = (params) => api.get(`${BASE}/recommendation-uploads/`, { params });
export const uploadRecommendationFile = (formData) => api.post(`${BASE}/recommendation-uploads/`, formData);
export const deleteRecommendationFile = (id) => api.delete(`${BASE}/recommendation-uploads/${id}/`);

// Observation uploads
export const getObservationUploads = (params) => api.get(`${BASE}/observation-uploads/`, { params });
export const uploadObservationFile = (formData) => api.post(`${BASE}/observation-uploads/`, formData);
export const deleteObservationFile = (id) => api.delete(`${BASE}/observation-uploads/${id}/`);
