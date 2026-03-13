// frontend/src/components/agronomy/AgronomyRoutes.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";

import AgronomyDashboard from "./AgronomyDashboard";
import AgronomyRecommendations from "./AgronomyRecommendations";
import AgronomyObservations from "./AgronomyObservations";

const AgronomyRoutes = () => {
  return (
    <Routes>
      <Route index element={<AgronomyDashboard />} />
      <Route path="recommendations" element={<AgronomyRecommendations />} />
      <Route path="observations" element={<AgronomyObservations />} />
    </Routes>
  );
};

export default AgronomyRoutes;

