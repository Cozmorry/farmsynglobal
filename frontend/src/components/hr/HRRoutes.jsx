// src/components/hr/HRRoutes.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";

import HRDashboard from "./pages/HRDashboard";

// Permanent Staff
import PermanentStaffList from "./pages/PermanentStaffList";
import PermanentStaffForm from "./forms/PermanentStaffForm";

// Casual Workers
import CasualWorkerList from "./pages/CasualWorkerList";
import CasualWorkerForm from "./forms/CasualWorkerForm";

// Work Sessions
import WorkSessionList from "./pages/WorkSessionList";
import WorkSessionForm from "./forms/WorkSessionForm";

// Payroll
import PayrollList from "./pages/PayrollList";
import PayrollGenerateForm from "./forms/PayrollGenerateForm";

// Payments
import HRPaymentList from "./pages/HRPaymentList";
import HRPaymentForm from "./forms/HRPaymentForm";

const HRRoutes = () => {
  return (
    <Routes>
      <Route index element={<HRDashboard />} />

      {/* Permanent Staff */}
      <Route path="permanent" element={<PermanentStaffList />} />
      <Route path="permanent/new" element={<PermanentStaffForm />} />
      <Route path="permanent/edit/:id" element={<PermanentStaffForm />} />

      {/* Casual Workers */}
      <Route path="casual" element={<CasualWorkerList />} />
      <Route path="casual/new" element={<CasualWorkerForm />} />
      <Route path="casual/edit/:id" element={<CasualWorkerForm />} />

      {/* Work Sessions */}
      <Route path="work-sessions" element={<WorkSessionList />} />
      <Route path="work-sessions/new" element={<WorkSessionForm />} />

      {/* Payroll */}
      <Route path="payroll" element={<PayrollList />} />
      <Route path="payroll/generate" element={<PayrollGenerateForm />} />

      {/* HR Payments */}
      <Route path="payments" element={<HRPaymentList />} />
      <Route path="payments/new" element={<HRPaymentForm />} />
    </Routes>
  );
};

export default HRRoutes;

