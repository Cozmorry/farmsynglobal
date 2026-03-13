// src/components/livestock/LivestockRoutes.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

/* ======================
   DASHBOARD
====================== */
import LivestockDashboard from "./pages/LivestockDashboard";

/* ======================
   CORE ENTITIES
====================== */
import LivestockList from "./pages/LivestockList";
import LivestockForm from "./forms/LivestockForm";

import LivestockGroupList from "./pages/LivestockGroupList";
import LivestockGroupForm from "./forms/LivestockGroupForm";

/* ======================
   LIST PAGES (SUBMODULES)
====================== */
import LivestockWeightList from "./pages/LivestockWeightList";
import LivestockBreedingList from "./pages/LivestockBreedingList";
import LivestockProductionList from "./pages/LivestockProductionList";
import LivestockFeedingList from "./pages/LivestockFeedingList";
import LivestockActivityList from "./pages/LivestockActivityList";
import LivestockExpenseList from "./pages/LivestockExpenseList";
import LivestockSalesList from "./pages/LivestockSalesList";

/* ======================
   GENERIC SUBMODULE FORMS
====================== */
import LivestockSubmoduleCreate from "./pages/LivestockSubmoduleCreate";
import LivestockSubmoduleEdit from "./pages/LivestockSubmoduleEdit";

const LivestockRoutes = () => {
  return (
    <Routes>
      {/* Base */}
      <Route index element={<Navigate to="dashboard" replace />} />

      {/* Dashboard */}
      <Route path="dashboard" element={<LivestockDashboard />} />

      {/* Livestock (Animals) */}
      <Route path="animals" element={<LivestockList />} />
      <Route path="animals/new" element={<LivestockForm />} />
      <Route path="animals/edit/:id" element={<LivestockForm />} />

      {/* Groups / Herds */}
      <Route path="groups" element={<LivestockGroupList />} />
      <Route path="groups/new" element={<LivestockGroupForm />} />

      {/* Submodule List Pages */}
      <Route path="weights" element={<LivestockWeightList />} />
      <Route path="breeding" element={<LivestockBreedingList />} />
      <Route path="productions" element={<LivestockProductionList />} />
      <Route path="feeding" element={<LivestockFeedingList />} />
      <Route path="activities" element={<LivestockActivityList />} />
      <Route path="expenses" element={<LivestockExpenseList />} />
      <Route path="sales" element={<LivestockSalesList />} />

      {/* Generic Submodule Create / Edit */}
      <Route path=":submodule/new" element={<LivestockSubmoduleCreate />} />
      <Route
        path=":submodule/edit/:id"
        element={<LivestockSubmoduleEdit />}
      />
    </Routes>
  );
};

{/* BARN CONTEXT DASHBOARD */}
<Route
  path="barns/:barnId"
  element={<LivestockDashboard />}
/>

export default LivestockRoutes;
