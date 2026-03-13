// src/components/weather/WeatherRecords.jsx
import React, { useEffect, useState } from "react";
import { Box, Typography, Paper, CircularProgress, Divider } from "@mui/material";
import { getCurrentWeather } from "./api/weatherApi";

const WeatherCurrent = ({ farmId }) => {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        const res = await getCurrentWeather(farmId);
        setWeather(res.data);
      } catch (err) {
        console.error("Failed to fetch weather", err);
      } finally {
        setLoading(false);
      }
    };
    fetchWeather();
  }, [farmId]);

  if (loading) return <CircularProgress />;
  if (!weather) return <Typography>No weather data</Typography>;

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" mb={2}>🌤 Current Weather</Typography>

      <Typography>🌡 Temperature: {weather.temperature} °C</Typography>
      <Typography>💧 Humidity: {weather.humidity} %</Typography>
      <Typography>🌧 Rainfall: {weather.rainfall || 0} mm</Typography>
      <Typography>🌬 Wind Speed: {weather.wind_speed} m/s</Typography>
      <Typography>🧭 Wind Direction: {weather.wind_direction}°</Typography>
      <Typography>📖 Condition: {weather.description}</Typography>

      <Divider sx={{ my: 2 }} />

      {/* AGRONOMY IMPACT */}
      <Typography variant="h6">🌱 Agronomy Impact</Typography>
      {weather.rainfall > 15 && (
        <Typography color="error">⚠️ High fungal disease risk</Typography>
      )}
      {weather.humidity > 80 && (
        <Typography color="warning.main">⚠️ Mildew risk due to humidity</Typography>
      )}
      {weather.temperature > 32 && (
        <Typography color="warning.main">⚠️ Increased irrigation demand</Typography>
      )}

      <Divider sx={{ my: 2 }} />

      {/* VETERINARY IMPACT */}
      <Typography variant="h6">🐄 Veterinary Impact</Typography>
      {weather.temperature > 35 && (
        <Typography color="error">⚠️ Heat stress risk in livestock</Typography>
      )}
      {weather.humidity > 80 && (
        <Typography color="warning.main">⚠️ Respiratory disease risk</Typography>
      )}
      {weather.temperature < 5 && (
        <Typography color="error">⚠️ Cold stress risk in poultry</Typography>
      )}
    </Paper>
  );
};

export default WeatherCurrent;


