// src/components/poultry/api/poultryApi.js

import api from "../../../api/axios"; // Axios instance

const BASE = "/api/poultry";

/* =====================================================
   BATCHES
===================================================== */

export const getBatches = (params = {}) =>
  api.get(`${BASE}/batches`, { params });

export const getBatch = (id) =>
  api.get(`${BASE}/batches/${id}`);

export const createBatch = (data) =>
  api.post(`${BASE}/batches`, data);

export const updateBatch = (id, data) =>
  api.patch(`${BASE}/batches/${id}`, data);

export const deleteBatch = (id) =>
  api.delete(`${BASE}/batches/${id}`);

export const restoreBatch = (id) =>
  api.put(`${BASE}/batches/${id}/restore`);


/* =====================================================
   ACTIVITIES (FEED, VACCINE, MORTALITY, ETC.)
===================================================== */

export const getActivities = (params = {}) =>
  api.get(`${BASE}/activities`, { params });

export const getActivity = (id) =>
  api.get(`${BASE}/activities/${id}`);

export const createActivity = (data) =>
  api.post(`${BASE}/activities`, data);

export const updateActivity = (id, data) =>
  api.patch(`${BASE}/activities/${id}`, data);

export const deleteActivity = (id) =>
  api.delete(`${BASE}/activities/${id}`);


/* =====================================================
   PRODUCTIONS (EGGS, MEAT, ETC.)
===================================================== */

export const getProductions = (params = {}) =>
  api.get(`${BASE}/production`, { params });

export const getProduction = (id) =>
  api.get(`${BASE}/production/${id}`);

export const createProduction = (data) =>
  api.post(`${BASE}/production`, data);

export const updateProduction = (id, data) =>
  api.patch(`${BASE}/production/${id}`, data);

export const deleteProduction = (id) =>
  api.delete(`${BASE}/production/${id}`);


/* =====================================================
   SALES
===================================================== */

export const getSales = (params = {}) =>
  api.get(`${BASE}/sales`, { params });

export const getSale = (id) =>
  api.get(`${BASE}/sales/${id}`);

export const createSale = (data) =>
  api.post(`${BASE}/sales`, data);

export const updateSale = (id, data) =>
  api.patch(`${BASE}/sales/${id}`, data);

export const deleteSale = (id) =>
  api.delete(`${BASE}/sales/${id}`);


/* =====================================================
   REPORTS
===================================================== */

export const exportPoultryReportPDF = () =>
  api.get(`${BASE}/export/pdf`, {
    responseType: "blob",
  });


/* =====================================================
   OPTIONAL: SAFE API CALL WRAPPER
===================================================== */

export const safeApiCall = async (apiCall) => {
  try {
    const res = await apiCall();
    return res.data;
  } catch (err) {
    console.error("Poultry API Error:", err);
    throw err;
  }
};
