// src/components/crop-management/api/cropManagementApi.js
import api from "../../../api/axios";


/* ======================================================
   CROPS
====================================================== */
export const getCrops = (params) =>
  api.get(`/crops/`, { params });

export const getCrop = (id) =>
  api.get(`${BASE}/crops/${id}`);

export const createCrop = (data) =>
  api.post(`/crops/`, data);

export const updateCrop = (id, data) =>
  api.put(`/crops/${id}`, data);

/* ======================================================
   ACTIVITY FACTORY (IMPORTANT)
====================================================== */
const activity = (type) => ({
  list: (params) =>
    api.get(`/activities/${type}/`, { params }),

  create: (data) =>
    api.post(`/activities/${type}/`, data),

  update: (id, data) =>
    api.put(`/activities/${type}/${id}`, data),

  remove: (id) =>
    api.delete(`/activities/${type}/${id}`),
});

/* ======================================================
   ACTIVITIES
====================================================== */
export const generalActivities = activity("general-activities");
export const nurseryActivities = activity("nursery-activities");
export const chemicalApplications = activity("chemical-applications");
export const fertilizerApplications = activity("fertilizer-applications");
export const weedingActivities = activity("weeding-activities");
export const scoutingActivities = activity("scouting-activities");
export const soilTests = activity("soil-tests");
export const soilAmendments = activity("soil-amendments");
export const cropRotations = activity("crop-rotations");
export const landPreparations = activity("land-preparations");

/* ======================================================
   HARVESTS
====================================================== */
export const getHarvests = (id) =>
  api.get(`/harvests/${id}`);

export const createHarvest = (data) =>
  api.post(`/harvests/`, data);

export const updateHarvest = (id, data) =>
  api.put(`/harvests/${id}`, data);

export const deleteHarvest = (id) =>
  api.delete(`/harvests/${id}`);


/* ======================================================
   SALES
====================================================== */
export const getSales = (params) =>
  api.get(`/sales/`, { params });

export const createSale = (data) =>
  api.post(`/sales/`, data);

export const updateSale = (id, data) =>
  api.put(`/sales/${id}`, data);

export const deleteSale = (id) =>
  api.delete(`/sales/${id}`);


/* ======================================================
   UPLOADS
====================================================== */
export const uploadActivityFile = (formData) =>
  api.post(`/uploads/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

export const getUploads = (params) =>
  api.get(`/uploads/`, { params });
