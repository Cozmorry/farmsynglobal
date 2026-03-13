// src/components/Navigation.jsx
import React, { useContext, useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { UsersContext } from "../context/UsersContext";
import { TenantContext } from "../context/TenantContext";
import api from "../api/axios";

const MODULE_LINKS = {
  crop: "/crop_management",
  agronomy: "/agronomy",
  livestock: "/livestock",
  veterinary: "/veterinary",
  poultry: "/poultry",
  aquaculture: "/aquaculture",
  finance: "/finance",
  store_inventory: "/store-inventory",
  hr: "/hr",
};

export default function Navigation() {
  const { tenants, currentTenant, switchTenant } = useContext(TenantContext);
  const { user, currentFarm, switchFarm } = useContext(UsersContext);

  const [activeModules, setActiveModules] = useState([]);
  const location = useLocation();
  const navigate = useNavigate();
  const isLoggedIn = !!user;

  // =============================
  // LOAD ACTIVE MODULES FOR CURRENT FARM
  // =============================
  useEffect(() => {
    if (!currentFarm?.id) {
      setActiveModules([]);
      return;
    }

    setActiveModules(currentFarm.active_modules ?? []);
  }, [currentFarm?.id, currentFarm?.active_modules]);

  // =============================
  // HANDLE SWITCH
  // =============================
  const handleFarmSwitch = (e) => {
    const farmId = e.target.value;
    switchFarm(farmId);
    navigate(`/farms/${farmId}`);
  };

  const handleTenantSwitch = (e) => {
    const tenantId = e.target.value;
    switchTenant(tenantId);
    localStorage.removeItem("current_farm_id");
    navigate("/");
  };

  // =============================
  // RENDER
  // =============================
  return (
    <nav style={{ padding: "10px", background: "#f8f8f8", marginBottom: "10px" }}>
      <Link to="/">Home</Link>

      {activeModules.map((mod) =>
        MODULE_LINKS[mod] ? (
          <React.Fragment key={mod}>
            {" | "}
            <Link to={MODULE_LINKS[mod]}>
              {mod.replace("_", " ").toUpperCase()}
            </Link>
          </React.Fragment>
        ) : null
      )}

      {!isLoggedIn ? (
        <>
          {" | "} <Link to="/login">Login</Link>
          {" | "} <Link to="/register">Register</Link>
        </>
      ) : (
        <>
          {" | "}
          <span>Welcome, {user?.username}</span>

          {tenants?.length > 0 && (
            <>
              {" | "}
              <select value={currentTenant?.id || ""} onChange={handleTenantSwitch}>
                <option value="">Select Tenant</option>
                {tenants.map((tenant) => (
                  <option key={tenant.id} value={tenant.id}>
                    {tenant.name}
                  </option>
                ))}
              </select>
            </>
          )}

          {user?.farms?.length > 0 && (
            <>
              {" | "}
              <select value={currentFarm?.id || ""} onChange={handleFarmSwitch}>
                <option value="">Select Farm</option>
                {user.farms.map((farm) => (
                  <option key={farm.id} value={farm.id}>
                    {farm.name}
                  </option>
                ))}
              </select>
            </>
          )}

          {user?.role === "owner" && (
            <>
              {" | "}
              <Link to="/farms/create">Create Farm</Link>
            </>
          )}
        </>
      )}
    </nav>
  );
}