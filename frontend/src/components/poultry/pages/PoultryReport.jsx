//src/components/poultry/pages/PoultryReport.jsx
import React from "react";
import { Button, Box, Typography } from "@mui/material";
import { exportPoultryReportPDF } from "../api/poultryApi";

export default function PoultryReport() {
  const handleDownload = async () => {
    try {
      const response = await exportPoultryReportPDF();
      const url = window.URL.createObjectURL(
        new Blob([response.data], { type: "application/pdf" })
      );
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "poultry_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Failed to download PDF:", error);
      alert("Failed to download PDF");
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Poultry Report
      </Typography>

      <Button variant="contained" onClick={handleDownload}>
        Download PDF
      </Button>
    </Box>
  );
}
