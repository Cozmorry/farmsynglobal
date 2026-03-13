// src/components/weather/api/weatherApi.js
import api from "../../../api/axios";

// CURRENT WEATHER (fetches + saves snapshot)
export const getCurrentWeather = (farmId) =>
  api.get(`/weather/farm/${farmId}/current`);

// WEATHER HISTORY
export const getWeatherHistory = (farmId, period = "7d") =>
  api.get(`/weather/farm/${farmId}/history`, {
    params: { period },
  });




