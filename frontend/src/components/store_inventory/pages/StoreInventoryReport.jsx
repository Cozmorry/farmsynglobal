// src/components/store_inventory/pages/StoreInventoryReport.jsx

import React from "react";
import { exportStoreInventoryPDF } from "../api/storeInventoryApi";

const StoreInventoryReport = () => {
  const handleDownload = async () => {
    try {
      const response = await exportStoreInventoryPDF();
      const url = window.URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "store_inventory_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Failed to download PDF:", error);
      alert("Failed to download PDF");
    }
  };

  return (
    <div>
      <h2>Store Inventory Report</h2>
      <button onClick={handleDownload}>Download PDF</button>
    </div>
  );
};

export default StoreInventoryReport;
