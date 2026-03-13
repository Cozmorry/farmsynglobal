// src/components/weather/WeatherRoutes.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";
import WeatherDashboard from "./WeatherDashboard";

const WeatherRoutes = () => {
  return (
    <Routes>
      <Route index element={<WeatherDashboard />} />
    </Routes>
  );
};

export default WeatherRoutes;


