// src/components/layout/MainLayout.jsx
import React from "react";
import SidebarPro from "./SidebarPro";
import { Outlet } from "react-router-dom";

export default function MainLayout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      {/* Sidebar */}
      <SidebarPro />

      {/* Main content */}
      <div style={{ flex: 1, padding: "20px", background: "#f1f2f6" }}>
        <Outlet /> {/* Renders the current route/page */}
      </div>
    </div>
  );
}
