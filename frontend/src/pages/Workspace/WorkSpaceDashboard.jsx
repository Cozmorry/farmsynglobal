//src/components/Farms/WorkspaceDashboard.jsx
import React, { useEffect, useState, useContext } from "react";
import { UsersContext } from "../../context/UsersContext";
import { TenantContext } from "../../context/TenantContext";
import api from "../../api/axios";
import { Link } from "react-router-dom";
import {
  FaLeaf,
  FaBook,
  FaCow,
  FaStethoscope,
  FaEgg,
  FaFish,
  FaMoneyBill,
  FaStore,
  FaUsers
} from "react-icons/fa6";

const MODULE_ICONS = {
  crop: <FaLeaf />,
  agronomy: <FaBook />,
  livestock: <FaCow />,
  veterinary: <FaStethoscope />,
  poultry: <FaEgg />,
  aquaculture: <FaFish />,
  finance: <FaMoneyBill />,
  store_inventory: <FaStore />,
  hr: <FaUsers />,
};

export default function WorkspaceDashboard() {
  const { currentFarm } = useContext(UsersContext);
  const { currentTenant } = useContext(TenantContext);

  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentFarm?.id) {
      setModules([]);
      return;
    }

    const fetchModules = async () => {
      setLoading(true);
      try {
        const res = await api.get("/farms/workspace/farm", {
          params: { farm_id: currentFarm.id },
        });

        setModules(res.data.active_modules || []);
      } catch (err) {
        console.error("Failed to fetch workspace modules", err);
        setModules([]);
      } finally {
        setLoading(false);
      }
    };

    fetchModules();
  }, [currentFarm, currentTenant]);

  if (!currentFarm?.id) {
    return (
      <div>
        <h2>Workspace Dashboard</h2>
        <p>Please select a farm to view the workspace.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div>
        <h2>Workspace Dashboard</h2>
        <p>Loading workspace modules...</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Workspace Dashboard</h2>
      <p>
        Tenant: <strong>{currentTenant?.name || "N/A"}</strong> | Farm:{" "}
        <strong>{currentFarm.name}</strong>
      </p>

      {modules.length === 0 && (
        <p style={{ marginTop: "20px" }}>
          No active modules for this farm.
        </p>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "20px",
          marginTop: "20px",
        }}
      >
        {modules.map((mod) => (
          <Link
            key={mod}
            to={`/${mod}`}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              padding: "20px",
              background: "#ffffff",
              color: "#2f3640",
              borderRadius: "8px",
              textDecoration: "none",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
              transition: "0.2s ease",
            }}
          >
            <div style={{ fontSize: "32px", marginBottom: "10px" }}>
              {MODULE_ICONS[mod] || <FaLeaf />}
            </div>

            <div
              style={{
                fontWeight: "bold",
                textTransform: "capitalize",
              }}
            >
              {mod.replace("_", " ")}
            </div>

            <div
              style={{
                fontSize: "12px",
                marginTop: "6px",
                opacity: 0.7,
              }}
            >
              Open {mod.replace("_", " ")}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
