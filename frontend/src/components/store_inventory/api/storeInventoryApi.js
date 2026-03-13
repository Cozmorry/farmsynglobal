// src/components/store_inventory/api/storeInventoryApi.js

import api from "../../../api/axios"; // same pattern used in Finance module

// Base prefix for backend store-inventory module
const BASE = "/store-inventory";

// ===================================================================
// STORE ITEMS
// ===================================================================

// Get all store items
export const getStoreItems = () => api.get(`${BASE}/items`);

// Get single item
export const getStoreItem = (id) => api.get(`${BASE}/items/${id}`);

// Create item
export const createStoreItem = (data) => api.post(`${BASE}/items`, data);

// Update item
export const updateStoreItem = (id, data) =>
  api.patch(`${BASE}/items/${id}`, data);

// Soft delete
export const deleteStoreItem = (id) => api.delete(`${BASE}/items/${id}`);

// Restore deleted item
export const restoreStoreItem = (id) =>
  api.put(`${BASE}/items/${id}/restore`);


// ===================================================================
// INVENTORY TRANSACTIONS
// ===================================================================

// Get all transactions
export const getInventoryTransactions = () =>
  api.get(`${BASE}/transactions`);

// Get single transaction
export const getInventoryTransaction = (id) =>
  api.get(`${BASE}/transactions/${id}`);

// Create transaction
export const createInventoryTransaction = (data) =>
  api.post(`${BASE}/transactions`, data);

// Update transaction
export const updateInventoryTransaction = (id, data) =>
  api.patch(`${BASE}/transactions/${id}`, data);

// Delete transaction
export const deleteInventoryTransaction = (id) =>
  api.delete(`${BASE}/transactions/${id}`);


// ===================================================================
// EXPORT PDF
// ===================================================================
export const exportStoreInventoryPDF = () =>
  api.get(`${BASE}/export/pdf`, {
    responseType: "blob",
  });

