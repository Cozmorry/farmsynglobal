// src/components/hr/api/hrApi.js
import api from "../../../api/axios";

const BASE = "/hr";

// ==================================================
// PERMANENT STAFF
// ==================================================
export const getPermanentStaff = (farm_id) =>
  api.get(`${BASE}/permanent/list`, { params: { farm_id } });

export const getPermanentStaffById = (id) =>
  api.get(`${BASE}/permanent/list`, { params: { id } });

export const createPermanentStaff = (data) =>
  api.post(`${BASE}/permanent/add`, data);

export const updatePermanentStaff = (id, data) =>
  api.patch(`${BASE}/permanent/${id}`, data);

export const deactivatePermanentStaff = (id) =>
  api.delete(`${BASE}/permanent/${id}`);

// ==================================================
// CASUAL WORKERS
// ==================================================
export const getCasualWorkers = (farm_id) =>
  api.get(`${BASE}/casual/list`, { params: { farm_id } });

export const getCasualWorkerById = (id) =>
  api.get(`${BASE}/casual/list`, { params: { id } });

export const createCasualWorker = (data) =>
  api.post(`${BASE}/casual/add`, data);

export const updateCasualWorker = (id, data) =>
  api.patch(`${BASE}/casual/${id}`, data);

export const deactivateCasualWorker = (id) =>
  api.delete(`${BASE}/casual/${id}`);

// ==================================================
// HR WORK SESSIONS
// ==================================================
export const getWorkSessions = (params) =>
  api.get(`${BASE}/work-session/list`, { params });

export const createWorkSession = (data) =>
  api.post(`${BASE}/work-session`, data);

// ==================================================
// HR PAYMENTS
// ==================================================
export const getHRPayments = (params) =>
  api.get(`${BASE}/payment/list`, { params });

export const createHRPayment = (data) =>
  api.post(`${BASE}/payment`, data);

// ==================================================
// PAYROLL
// ==================================================
export const getPayrolls = (employee_id) =>
  api.get(`${BASE}/payroll/list`, { params: { employee_id } });

export const generatePayroll = (employee_id, period_start, period_end) =>
  api.post(`${BASE}/payroll/generate/${employee_id}`, null, {
    params: { period_start, period_end },
  });
