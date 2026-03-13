// src/components/Layout.jsx
// src/components/Layout.jsx
import React, { useContext, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { UsersContext } from "../context/UsersContext";
import {
  FaHome,
  FaMoneyBill,
  FaBoxOpen,
  FaSeedling,
  FaLeaf,
  FaStethoscope,
  FaPaw,
  FaUsers,
} from "react-icons/fa";
import "./Layout.css";

export default function Layout({ children }) {
  const { user, logout, currentFarm } = useContext(UsersContext);
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  // If not logged in, don't render layout
  if (!user) return <>{children}</>;

  const links = [
    { path: "/", label: "Home", icon: <FaHome /> },
    { path: "/poultry", label: "Poultry", icon: <FaLeaf /> },
    { path: "/aquaculture", label: "Aquaculture", icon: <FaLeaf /> },
    { path: "/finance", label: "Finance", icon: <FaMoneyBill /> },
    { path: "/store-inventory", label: "Store Inventory", icon: <FaBoxOpen /> },
    { path: "/crop_management", label: "Crop Management", icon: <FaSeedling /> },
    { path: "/agronomy", label: "Agronomy", icon: <FaLeaf /> },
    { path: "/veterinary", label: "Veterinary", icon: <FaStethoscope /> },
    { path: "/livestock", label: "Livestock", icon: <FaPaw /> },
    { path: "/hr", label: "HR", icon: <FaUsers /> },
  ];

  return (
    <div className={`dashboard-container ${collapsed ? "collapsed" : ""}`}>
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-top">
          <h2>{collapsed ? "FS" : "Farmsynglobal"}</h2>
          {!collapsed && (
            <p className="farm-name">
              Farm: {currentFarm?.name || "No Farm Selected"}
            </p>
          )}

          <button
            className="collapse-btn"
            onClick={() => setCollapsed(!collapsed)}
          >
            {collapsed ? "➤" : "◀"}
          </button>
        </div>

        <nav className="sidebar-nav">
          {links.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              <span className="icon">{link.icon}</span>
              {!collapsed && <span>{link.label}</span>}
            </NavLink>
          ))}
        </nav>

        <button className="logout-btn" onClick={handleLogout}>
          {collapsed ? "⏻" : "Sign Out"}
        </button>
      </aside>

      {/* Main Content */}
      <main className="dashboard-main">
        <header className="dashboard-header">
          <p>Welcome, {user?.username}</p>
        </header>

        <div className="dashboard-content">{children}</div>
      </main>
    </div>
  );
}

