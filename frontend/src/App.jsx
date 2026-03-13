// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import CreateUser from "./pages/CreateUser";
import CreateFarm from "./pages/CreateFarm";
import WorkspaceDashboard from "./pages/Workspace/WorkSpaceDashboard";
import CreateTenantPage from "./pages/CreateTenantPage";
import TenantWizard from "./components/tenant/TenantWizard";

import CropManagementRoutes from "./components/crop-management/CropManagementRoutes";
import LivestockRoutes from "./components/livestock/LivestockRoutes";
import PoultryRoutes from "./components/poultry/PoultryRoutes";
import AquacultureRoutes from "./components/aquaculture/AquacultureRoutes";
import FinanceRoutes from "./components/finance/FinanceRoutes";
import StoreInventoryRoutes from "./components/store_inventory/StoreInventoryRoutes";
import HRRoutes from "./components/hr/HRRoutes";
import AgronomyRoutes from "./components/agronomy/AgronomyRoutes";
import VeterinaryRoutes from "./components/veterinary/VeterinaryRoutes";

import Navigation from "./components/Navigation";
import ProtectedRoute from "./components/layout/ProtectedRoute";
import MainLayout from "./components/layout/MainLayout";

import { UsersProvider } from "./context/UsersContext";
import { TenantProvider } from "./context/TenantContext";

export default function App() {
  return (
    <Router>
      <UsersProvider>
        <TenantProvider>
          {/* Global navigation bar */}
          <Navigation />

          <Routes>
            {/* Public routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<CreateUser />} />

            {/* Tenant onboarding */}
            <Route path="/create-tenant" element={<CreateTenantPage />} />
            <Route path="/tenants/onboard" element={<TenantWizard />} />

            {/* Protected routes with sidebar layout */}
            <Route element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
              <Route path="/workspace" element={<WorkspaceDashboard />} />

              {/* Module routes */}
              <Route path="/crop_management/*" element={<CropManagementRoutes />} />
              <Route path="/livestock/*" element={<LivestockRoutes />} />
              <Route path="/poultry/*" element={<PoultryRoutes />} />
              <Route path="/aquaculture/*" element={<AquacultureRoutes />} />
              <Route path="/finance/*" element={<FinanceRoutes />} />
              <Route path="/store-inventory/*" element={<StoreInventoryRoutes />} />
              <Route path="/hr/*" element={<HRRoutes />} />
              <Route path="/agronomy/*" element={<AgronomyRoutes />} />
              <Route path="/veterinary/*" element={<VeterinaryRoutes />} />

              {/* Farm creation */}
              <Route path="/farms/create" element={<CreateFarm />} />
            </Route>
          </Routes>
        </TenantProvider>
      </UsersProvider>
    </Router>
  );
}
