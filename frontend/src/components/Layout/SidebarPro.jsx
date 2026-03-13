// src/components/layout/SidebarPro.jsx
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

export default function SidebarPro() {
  const { tenants, currentTenant, switchTenant } = useContext(TenantContext);
  const { user, currentFarm, switchFarm } = useContext(UsersContext);

  const [activeModules, setActiveModules] = useState([]);
  const [collapsedModules, setCollapsedModules] = useState({});

  const location = useLocation();
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("access_token");

  // Fetch active modules for current farm
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
    navigate("/workspace");
  };

  const handleTenantSwitch = (e) => {
    switchTenant(e.target.value);
    localStorage.removeItem("current_farm_id");
    navigate("/");
  };

  const toggleCollapse = (mod) => {
    setCollapsedModules((prev) => ({
      ...prev,
      [mod]: !prev[mod],
    }));
  };

  return (
    <div
      style={{
        width: "250px",
        background: "#2f3640",
        color: "#fff",
        display: "flex",
        flexDirection: "column",
        padding: "20px",
      }}
    >
      <h2 style={{ marginBottom: "20px" }}>FarmSyn ERP</h2>

      {/* Tenant Selector */}
      {tenants?.length > 0 && (
        <div style={{ marginBottom: "15px" }}>
          <label>Tenant:</label>
          <select
            value={currentTenant?.id || ""}
            onChange={handleTenantSwitch}
            style={{ width: "100%", marginTop: "5px" }}
          >
            <option value="">Select Tenant</option>
            {tenants.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Farm Selector */}
      {user?.farms?.length > 0 && (
        <div style={{ marginBottom: "25px" }}>
          <label>Farm:</label>
          <select
            value={currentFarm?.id || ""}
            onChange={handleFarmSwitch}
            style={{ width: "100%", marginTop: "5px" }}
          >
            <option value="">Select Farm</option>
            {user.farms.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Modules */}
      <div style={{ flexGrow: 1 }}>
        <h4 style={{ marginBottom: "10px" }}>Modules</h4>
        <ul style={{ listStyle: "none", padding: 0 }}>
          {activeModules.map(
            (mod) =>
              MODULES[mod] && (
                <li key={mod} style={{ marginBottom: "8px" }}>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                      cursor: "pointer",
                      padding: "8px",
                      background: location.pathname.startsWith(
                        MODULES[mod].path
                      )
                        ? "#718093"
                        : "transparent",
                      borderRadius: "5px",
                      transition: "0.2s",
                    }}
                    onClick={() => toggleCollapse(mod)}
                  >
                    <span
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                      }}
                    >
                      {MODULES[mod].icon}
                      {MODULES[mod].label}
                    </span>
                    <span>{collapsedModules[mod] ? "+" : "-"}</span>
                  </div>

                  {!collapsedModules[mod] && (
                    <ul
                      style={{
                        listStyle: "none",
                        paddingLeft: "25px",
                        marginTop: "5px",
                      }}
                    >
                      <li>
                        <Link
                          to={MODULES[mod].path}
                          style={{
                            color: "#dcdde1",
                            textDecoration:
                              location.pathname === MODULES[mod].path
                                ? "underline"
                                : "none",
                          }}
                        >
                          Open {MODULES[mod].label}
                        </Link>
                      </li>
                    </ul>
                  )}
                </li>
              )
          )}
        </ul>
      </div>

      {/* User Info */}
      {isLoggedIn && (
        <div
          style={{
            marginTop: "auto",
            paddingTop: "20px",
            borderTop: "1px solid #57606f",
          }}
        >
          <p>Welcome, {user?.username || "User"}</p>
          {user?.role === "owner" && (
            <Link
              to="/farms/create"
              style={{ color: "#00a8ff", textDecoration: "none" }}
            >
              Create Farm
            </Link>
          )}
        </div>
      )}
    </div>
  );
}
