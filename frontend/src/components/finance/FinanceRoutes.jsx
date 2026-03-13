
// src/components/finance/FinanceRoutes.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

// PAGES
import FinanceHome from "./pages/FinanceHome"; // optional landing page for /finance
import FinanceList from "./pages/FinanceList";
import CreateFinanceEntry from "./forms/NewFinanceEntry";

import InvoiceList from "./pages/InvoiceList";
import NewInvoice from "./forms/NewInvoice";

import PaymentList from "./pages/PaymentList";
import NewPayment from "./forms/NewPayment";

import FinanceReport from "./pages/FinanceReport";

export default function FinanceRoutes() {
  return (
    <Routes>
      {/* Finance root redirects to home */}
      <Route path="/" element={<FinanceHome />} />

      {/* FINANCE ENTRIES */}
      <Route path="entries" element={<FinanceList />} />
      <Route path="entry/new" element={<CreateFinanceEntry />} />

      {/* INVOICES */}
      <Route path="invoices" element={<InvoiceList />} />
      <Route path="invoice/new" element={<NewInvoice />} />

      {/* PAYMENTS */}
      <Route path="payments" element={<PaymentList />} />
      <Route path="payment/new" element={<NewPayment />} />

      {/* FINANCE REPORT */}
      <Route path="report" element={<FinanceReport />} />

      {/* Fallback route: redirect unknown paths */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}
