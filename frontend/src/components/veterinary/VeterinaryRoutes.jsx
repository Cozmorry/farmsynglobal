// src/components/veterinary/VeterinaryRoutes.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";

import VeterinaryDashboard from "./VeterinaryDashboard";
import VeterinaryHealthRecords from "./VeterinaryHealthRecords";
import VeterinaryRecommendations from "./VeterinaryRecommendations";
import VeterinaryFileUpload from "./VeterinaryFileUpload";

export default function VeterinaryRoutes() {
  return (
    <Routes>
      <Route path="/" element={<VeterinaryDashboard />} />
      <Route path="health" element={<VeterinaryHealthRecords />} />
      <Route path="recommendations" element={<VeterinaryRecommendations />} />
      <Route path="uploads/:type/:id" element={<VeterinaryFileUpload />} />
    </Routes>
  );
}
