// src/components/poultry/PoultryRoutes.jsx
import React from "react";
import { Routes, Route, useParams } from "react-router-dom";

import PoultryDashboard from "./pages/PoultryDashboard";
import PoultryReport from "./pages/PoultryReport";

// Batches
import PoultryBatchList from "./pages/PoultryBatchList";
import PoultryBatchForm from "./forms/PoultryBatchForm";

// Activities
import PoultryActivityList from "./pages/PoultryActivityList";
import PoultryActivityForm from "./forms/PoultryActivityForm";

// Production
import PoultryProductionList from "./pages/PoultryProductionList";
import PoultryProductionForm from "./forms/PoultryProductionForm";

// Sales
import PoultrySaleList from "./pages/PoultrySaleList";
import PoultrySaleForm from "./forms/PoultrySaleForm";

const PoultryRoutes = () => {
  return (
    <Routes>
      {/* Dashboard */}
      <Route index element={<PoultryDashboard />} />
      <Route path="report" element={<PoultryReport />} />

      {/* Batches */}
      <Route path="batches" element={<PoultryBatchList />} />
      <Route path="batches/new" element={<PoultryBatchForm />} />
      <Route path="batches/edit/:id" element={<PoultryBatchForm />} />

      {/* 🔹 Batch-context routes (NEW, OPTIONAL) */}
      <Route
        path="batches/:batchId/activities"
        element={<BatchActivityWrapper />}
      />
      <Route
        path="batches/:batchId/productions"
        element={<BatchProductionWrapper />}
      />
      <Route
        path="batches/:batchId/sales"
        element={<BatchSalesWrapper />}
      />

      {/* Flat routes (existing) */}
      <Route path="activities" element={<PoultryActivityList />} />
      <Route path="activities/new" element={<PoultryActivityForm />} />
      <Route path="activities/edit/:id" element={<PoultryActivityForm />} />

      <Route path="productions" element={<PoultryProductionList />} />
      <Route path="productions/new" element={<PoultryProductionForm />} />
      <Route path="productions/edit/:id" element={<PoultryProductionForm />} />

      <Route path="sales" element={<PoultrySaleList />} />
      <Route path="sales/new" element={<PoultrySaleForm />} />
      <Route path="sales/edit/:id" element={<PoultrySaleForm />} />
    </Routes>
  );
};

export default PoultryRoutes;

/* ===================== */
/* Param Wrappers (NEW)  */
/* ===================== */

function BatchActivityWrapper() {
  const { batchId } = useParams();
  return <PoultryActivityList batchId={batchId} />;
}

function BatchProductionWrapper() {
  const { batchId } = useParams();
  return <PoultryProductionList batchId={batchId} />;
}

function BatchSalesWrapper() {
  const { batchId } = useParams();
  return <PoultrySaleList batchId={batchId} />;
}

{/* COOP CONTEXT DASHBOARD */}
<Route
  path="coops/:coopId"
  element={<PoultryDashboard />}
/>
