// src/components/store_inventory/StoreInventoryRoutes.jsx

import React from "react";
import { Routes, Route } from "react-router-dom";

import StoreInventoryDashboard from "./pages/StoreInventoryDashboard";
import StoreItemList from "./pages/StoreItemList";
import StoreItemForm from "./forms/StoreItemForm";
import InventoryTransactionList from "./pages/InventoryTransactionList";
import InventoryTransactionForm from "./forms/InventoryTransactionForm";

const StoreInventoryRoutes = () => {
  return (
    <Routes>
      <Route index element={<StoreInventoryDashboard />} />

      {/* Store Items */}
      <Route path="items" element={<StoreItemList />} />
      <Route path="items/new" element={<StoreItemForm />} />
      <Route path="items/edit/:id" element={<StoreItemForm />} />

      {/* Inventory Transactions */}
      <Route path="transactions" element={<InventoryTransactionList />} />
      <Route path="transactions/new" element={<InventoryTransactionForm />} />
      <Route path="transactions/edit/:id" element={<InventoryTransactionForm />} />
    </Routes>
  );
};

export default StoreInventoryRoutes;

