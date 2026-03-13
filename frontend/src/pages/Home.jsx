//src/pages/Home.jsx
// src/pages/Home.jsx
import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { UsersContext } from "../context/UsersContext";
import { TenantContext } from "../context/TenantContext"; // <-- import TenantContext
import KpiCard from "../components/ui/KpiCard";
import "./Home.css";

export default function Home() {
  const [farms, setFarms] = useState([]);
  const { user, logoutUser } = useContext(UsersContext);
  const { currentTenant } = useContext(TenantContext); // <-- get currentTenant
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) return;

    const fetchFarms = async () => {
      try {
        // ✅ Ensure tenant ID is in localStorage
        if (currentTenant) {
          localStorage.setItem("current_tenant_id", currentTenant.id);
        } else {
          console.warn("No tenant selected. Cannot fetch farms.");
          return;
        }

        const res = await api.get("/farms");
        setFarms(res.data);
      } catch (err) {
        console.error(err);
        logoutUser();
      }
    };

    fetchFarms();
  }, [user, currentTenant, logoutUser]); // <-- add currentTenant dependency

  if (!user) return null;

  const totalModules = farms.reduce(
    (acc, farm) => acc + (farm.active_modules?.length || 0),
    0
  );

  return (
    <div>
      {/* Hero Section */}
      <div
        style={{
          background: "linear-gradient(135deg, #3b82f6, #6366f1)",
          color: "white",
          padding: "30px",
          borderRadius: "16px",
          marginBottom: "30px",
        }}
      >
        <h2>Welcome back, {user.username} 👋</h2>
        <p>Manage your agricultural operations with precision and intelligence.</p>
      </div>

      {/* KPI Section */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <KpiCard title="Total Farms" value={farms.length} color="#3b82f6" />
        <KpiCard title="Active Modules" value={totalModules} color="#10b981" />
        <KpiCard title="User Role" value="Farm Owner" color="#f59e0b" />
      </div>

      {/* Farms Grid */}
      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <h3>Your Farms</h3>

          <button
            onClick={() => navigate("/farms/create")}
            style={{
              background: "#3b82f6",
              color: "white",
              border: "none",
              padding: "8px 14px",
              borderRadius: "8px",
              cursor: "pointer",
            }}
          >
            + Create Farm
          </button>
        </div>

        <div className="grid">
          {farms.map((farm) => (
            <div
              key={farm.id}
              className="farm-card"
              onClick={() => navigate(`/farms/${farm.id}`)}
            >
              <h4>{farm.name}</h4>
              <p>{farm.active_modules?.join(", ") || "No modules selected"}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}