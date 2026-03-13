// src/components/layout/SidebarMini.jsx
// src/components/layout/SidebarMini.jsx
import React, { useContext, useState, useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { UsersContext } from "../../context/UsersContext";
import { TenantContext } from "../../context/TenantContext";
import {
  FaLeaf,
  FaBook,
  FaCow,
  FaStethoscope,
  FaEgg,
  FaFish,
  FaMoneyBill,
  FaStore,
  FaUsers,
  FaBars,
} from "react-icons/fa6";
import api from "../../api/axios";

const MODULES = {
  crop: { path: "/crop_management", label: "Crop", icon: <FaLeaf /> },
  agronomy: { path: "/agronomy", label: "Agronomy", icon: <FaBook /> },
  livestock: { path: "/livestock", label: "Livestock", icon: <FaCow /> },
  veterinary: { path: "/veterinary", label: "Veterinary", icon: <FaStethoscope /> },
  poultry: { path: "/poultry", label: "Poultry", icon: <FaEgg /> },
  aquaculture: { path: "/aquaculture", label: "Aquaculture", icon: <FaFish /> },
  finance: { path: "/finance", label: "Finance", icon: <FaMoneyBill /> },
  store_inventory: { path: "/store-inventory", label: "Store", icon: <FaStore /> },
  hr: { path: "/hr", label: "HR", icon: <FaUsers /> },
};

export default function SidebarMini() {
  const { tenants, currentTenant, switchTenant } = useContext(TenantContext);
  const { user, currentFarm, switchFarm } = useContext(UsersContext);

  const [activeModules, setActiveModules] = useState([]);
  const [collapsed, setCollapsed] = useState(true);

  const location = useLocation();
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("access_token");

  useEffect(() => {
    if (!isLoggedIn || !currentFarm?.id) {
      setActiveModules([]);
      return;
    }

    const fetchModules = async () => {
      try {
        const res = await api.get("/farms/workspace/farm", {
          params: { farm_id: currentFarm.id },
        });
        setActiveModules(res.data.active_modules || []);
      } catch (err) {
        console.error("Failed to load active modules", err);
        setActiveModules([]);
      }
    };

    fetchModules();
  }, [currentFarm, currentTenant, isLoggedIn]);

  const handleFarmSwitch = (e) => {
    switchFarm(e.target.value);
    navigate(`/workspace`);
  };

  return (
    <div
      style={{
        width: collapsed ? "60px" : "220px",
        minHeight: "100vh",
        background: "#2f3640",
        color: "#fff",
        display: "flex",
        flexDirection: "column",
        transition: "width 0.2s",
      }}
      onMouseEnter={() => setCollapsed(false)}
      onMouseLeave={() => setCollapsed(true)}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: collapsed ? "center" : "space-between",
          padding: "15px",
        }}
      >
        {!collapsed && <h2 style={{ fontSize: "18px" }}>FarmSyn</h2>}
        <FaBars size={20} />
      </div>

      {/* Modules */}
      <ul style={{ listStyle: "none", padding: 0, flexGrow: 1 }}>
        {activeModules.map(
          (mod) =>
            MODULES[mod] && (
              <li key={mod} style={{ marginBottom: "10px" }}>
                <Link
                  to={MODULES[mod].path}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                    padding: "10px",
                    color: location.pathname.startsWith(
                      MODULES[mod].path
                    )
                      ? "#00a8ff"
                      : "#dcdde1",
                    textDecoration: "none",
                    borderRadius: "5px",
                    justifyContent: collapsed
                      ? "center"
                      : "flex-start",
                    transition: "0.2s",
                  }}
                  title={MODULES[mod].label}
                >
                  {MODULES[mod].icon}
                  {!collapsed && MODULES[mod].label}
                </Link>
              </li>
            )
        )}
      </ul>

      {/* Tenant & Farm Selectors */}
      {!collapsed && (
        <div
          style={{
            padding: "15px",
            borderTop: "1px solid #57606f",
          }}
        >
          {tenants?.length > 0 && (
            <select
              value={currentTenant?.id || ""}
              onChange={(e) => switchTenant(e.target.value)}
              style={{ width: "100%", marginBottom: "10px" }}
            >
              {tenants.map((tenant) => (
                <option key={tenant.id} value={tenant.id}>
                  {tenant.name}
                </option>
              ))}
            </select>
          )}

          {user?.farms?.length > 0 && (
            <select
              value={currentFarm?.id || ""}
              onChange={handleFarmSwitch}
              style={{ width: "100%" }}
            >
              {user.farms.map((farm) => (
                <option key={farm.id} value={farm.id}>
                  {farm.name}
                </option>
              ))}
            </select>
          )}
        </div>
      )}
    </div>
  );
}
