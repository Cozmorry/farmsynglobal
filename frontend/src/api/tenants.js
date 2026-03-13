// src/api/tenants.js
import api from "./axios";

export async function getTenants() {
  const res = await api.get("/tenants");
  return res.data;
}

export async function createTenant(data) {
  const res = await api.post("/tenants/create", data);
  return res.data;
}

export async function assignModules(tenantId, modules) {
  const res = await api.put(`/tenants/${tenantId}/modules`, modules);
  return res.data;
}
