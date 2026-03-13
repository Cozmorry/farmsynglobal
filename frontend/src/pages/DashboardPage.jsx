// src/pages/DashboardPage.jsx
import { useContext } from "react";
import { UsersContext } from "@/context/UsersContext";
import { Navigate } from "react-router-dom";
import DashboardCard from "@/components/DashboardCard";

export default function DashboardPage() {
  const { user, currentFarm } = useContext(UsersContext);

  if (!user) return <Navigate to="/login" />;

  return (
    <div>
      <h1 style={{ marginBottom: 20 }}>Welcome back, {user.username || user.email}</h1>
      <p style={{ marginBottom: 30 }}>
        {currentFarm ? `Current Farm: ${currentFarm.name}` : "No farm selected"}
      </p>

      <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
        {/* Example dashboard cards */}
        <DashboardCard title="Livestock Count" value={user.stats?.livestock || 0} />
        <DashboardCard title="Crops Planted" value={user.stats?.crops || 0} />
        <DashboardCard title="Pending Tasks" value={user.stats?.tasks || 0} />
        <DashboardCard title="Notifications" value={user.stats?.notifications || 0} />
      </div>
    </div>
  );
}
