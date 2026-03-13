// src/components/livestock/api/livestockApi.js
import api from "../../../api/axios";

// Base prefix
const BASE = "/api/livestock";

/* ==============================
   LIVESTOCK (MASTER)
============================== */
export const livestock = {
  list: () => api.get(`${BASE}/`),
  get: (id) => api.get(`${BASE}/${id}`),
  create: (data) => api.post(`${BASE}/`, data),
  update: (id, data) => api.put(`${BASE}/${id}`, data),
  delete: (id) => api.delete(`${BASE}/${id}`),
};

/* ==============================
   GROUPS / HERDS
============================== */
export const groups = {
  list: () => api.get(`${BASE}/groups/`),
  create: (data) => api.post(`${BASE}/groups/`, data),
  assign: (groupId, livestockId) =>
    api.put(`${BASE}/groups/${groupId}/assign/${livestockId}`),
};

/* ==============================
   WEIGHT RECORDS
============================== */
export const weights = {
  list: () => api.get(`${BASE}/weights/`),
  get: (id) => api.get(`${BASE}/weights/${id}`),
  create: (data) => api.post(`${BASE}/weights/`, data),
  update: (id, data) => api.put(`${BASE}/weights/${id}`, data),
  delete: (id) => api.delete(`${BASE}/weights/${id}`),
};

/* ==============================
   BREEDING RECORDS
============================== */
export const breeding = {
  list: () => api.get(`${BASE}/breeding/`),
  get: (id) => api.get(`${BASE}/breeding/${id}`),
  create: (data) => api.post(`${BASE}/breeding/`, data),
  update: (id, data) => api.put(`${BASE}/breeding/${id}`, data),
  delete: (id) => api.delete(`${BASE}/breeding/${id}`),
};

/* ==============================
   PRODUCTIONS
============================== */
export const productions = {
  list: () => api.get(`${BASE}/productions/`),
  get: (id) => api.get(`${BASE}/productions/${id}`),
  create: (data) => api.post(`${BASE}/productions/`, data),
  update: (id, data) => api.put(`${BASE}/productions/${id}`, data),
  delete: (id) => api.delete(`${BASE}/productions/${id}`),
};

/* ==============================
   FEEDING
============================== */
export const feedings = {
  list: () => api.get(`${BASE}/feeding/`),
  get: (id) => api.get(`${BASE}/feeding/${id}`),
  create: (data) => api.post(`${BASE}/feeding/`, data),
  update: (id, data) => api.put(`${BASE}/feeding/${id}`, data),
  delete: (id) => api.delete(`${BASE}/feeding/${id}`),
};

/* ==============================
   ACTIVITIES
============================== */
export const activities = {
  list: () => api.get(`${BASE}/activities/`),
  get: (id) => api.get(`${BASE}/activities/${id}`),
  create: (data) => api.post(`${BASE}/activities/`, data),
  update: (id, data) => api.put(`${BASE}/activities/${id}`, data),
  delete: (id) => api.delete(`${BASE}/activities/${id}`),
};

/* ==============================
   EXPENSES
============================== */
export const expenses = {
  list: () => api.get(`${BASE}/expenses/`),
  get: (id) => api.get(`${BASE}/expenses/${id}`),
  create: (data) => api.post(`${BASE}/expenses/`, data),
  update: (id, data) => api.put(`${BASE}/expenses/${id}`, data),
  delete: (id) => api.delete(`${BASE}/expenses/${id}`),
};

/* ==============================
   SALES
============================== */
export const sales = {
  list: () => api.get(`${BASE}/sales/`),
  get: (id) => api.get(`${BASE}/sales/${id}`),
  create: (data) => api.post(`${BASE}/sales/`, data),
  update: (id, data) => api.put(`${BASE}/sales/${id}`, data),
  delete: (id) => api.delete(`${BASE}/sales/${id}`),
};

/* ==============================
   DEFAULT EXPORT (OPTIONAL)
============================== */
export default {
  livestock,
  groups,
  weights,
  breeding,
  productions,
  feedings,
  activities,
  expenses,
  sales,
};

