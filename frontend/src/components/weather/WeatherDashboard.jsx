// src/components/weather/WeatherDashboard.jsx
import React, { useEffect, useState } from "react";
import { Box, Typography, CircularProgress } from "@mui/material";
import WeatherCurrent from "./WeatherCurrent";
import WeatherHistory from "./WeatherHistory";
import api from "../../api";

const WeatherDashboard = () => {
  const [farmId, setFarmId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFarm = async () => {
      const res = await api.get("/farms/");
      if (res.data.length > 0) {
        setFarmId(res.data[0].id);
      }
      setLoading(false);
    };
    loadFarm();
  }, []);

  if (loading) return <CircularProgress />;
  if (!farmId) return <Typography>No farm found</Typography>;

  // Temporary mock history
  const mockHistory = [
    { time: "06:00", temperature: 22, humidity: 70 },
    { time: "09:00", temperature: 26, humidity: 65 },
    { time: "12:00", temperature: 32, humidity: 55 },
    { time: "15:00", temperature: 35, humidity: 50 },
    { time: "18:00", temperature: 30, humidity: 60 },
  ];

  return (
    <Box p={3}>
      <Typography variant="h3" mb={3}>Weather Dashboard</Typography>

      <WeatherCurrent farmId={farmId} />
      <WeatherHistory history={mockHistory} />
    </Box>
  );
};

export default WeatherDashboard;


