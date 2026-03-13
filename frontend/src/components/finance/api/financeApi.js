// src/components/finance/api/financeApi.js
import axios from "axios";

const API_URL = "/api/financeApi"; 

// ======== FINANCE ENTRY ========
export const createFinanceEntry = (data) => axios.post(`${API_URL}/entry`, data);
export const getFinanceEntry = (id) => axios.get(`${API_URL}/entry/${id}`);

// ======== FINANCIAL SUMMARY ========
export const getFinancialSummary = (params) =>
  axios.get(`${API_URL}/summary`, { params });

// ======== INVOICES ========
// Fetch multiple invoices, optionally filtered by farm_id or other params
export const getInvoices = (params) => 
  axios.get(`${API_URL}/invoice`, { params });

export const createInvoice = (data) => axios.post(`${API_URL}/invoice`, data);
export const getInvoice = (id) => axios.get(`${API_URL}/invoice/${id}`);

// ======== PAYMENTS ========
export const createPayment = (data) => axios.post(`${API_URL}/payment`, data);
export const getPayment = (id) => axios.get(`${API_URL}/payment/${id}`);

// ======== EXPORT (PDF/Excel) ========
export const exportFinance = (type = "pdf", params) =>
  axios.get(`${API_URL}/export/${type}`, { params, responseType: "blob" });

export const exportFinanceTable = (table, params) =>
  axios.get(`${API_URL}/export/${table}`, { params, responseType: "blob" });

