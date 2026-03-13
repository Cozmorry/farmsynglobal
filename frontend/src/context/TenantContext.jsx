//src/context/TenantContext.jsx
import React, { createContext, useEffect, useState } from "react";
import { getTenants } from "../api/tenants";

export const TenantContext = createContext(null);

export const TenantProvider = ({ children }) => {
  const [tenants, setTenants] = useState([]);
  const [currentTenant, setCurrentTenant] = useState(null);

  // =============================
  // LOAD TENANTS
  // =============================
  useEffect(() => {
    const loadTenants = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) return;

      try {
        const data = await getTenants();
        setTenants(data);

        const storedTenant = localStorage.getItem("current_tenant_id");
        if (storedTenant) {
          const found = data.find(t => t.id === Number(storedTenant));
          setCurrentTenant(found || null);
        }
      } catch (err) {
        console.error("Failed to load tenants:", err);
      }
    };

    loadTenants();
  }, []);

  // =============================
  // SWITCH TENANT
  // =============================
  const switchTenant = (tenantId) => {
    const found = tenants.find(t => t.id === Number(tenantId));
    if (!found) return;
    setCurrentTenant(found);
    localStorage.setItem("current_tenant_id", found.id);
  };

  return (
    <TenantContext.Provider value={{ tenants, currentTenant, switchTenant }}>
      {children}
    </TenantContext.Provider>
  );
};