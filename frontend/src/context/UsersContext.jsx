// src/context/UsersContext.jsx
import React, { createContext, useState, useEffect } from "react";
import api from "../api/axios";

const UsersContext = createContext(null);

const UsersProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [currentFarm, setCurrentFarm] = useState(null);

  // =============================
  // REFRESH FARMS
  // =============================
  const refreshFarms = async () => {
    try {
      const res = await api.get("/farms");
      const updatedUser = { ...user, farms: res.data };
      setUser(updatedUser);
      localStorage.setItem("user_data", JSON.stringify(updatedUser));
    } catch (err) {
      console.error("Failed to refresh farms", err);
    }
  };

  // =============================
  // UPDATE SINGLE FARM LOCALLY
  // =============================
  const updateFarm = (updatedFarm) => {
    if (!user?.farms) return;

    const updatedFarms = user.farms.map((f) =>
      f.id === updatedFarm.id ? { ...f, ...updatedFarm } : f
    );

    const updatedUser = { ...user, farms: updatedFarms };
    setUser(updatedUser);

    // Update currentFarm if it was the one updated
    if (currentFarm?.id === updatedFarm.id) {
      setCurrentFarm({ ...currentFarm, ...updatedFarm });
    }

    localStorage.setItem("user_data", JSON.stringify(updatedUser));
  };

  // =============================
  // LOGIN
  // =============================
  const loginUser = async ({ identifier, password }) => {
    try {
      const response = await api.post("/login", { identifier, password });
      const { access_token, user } = response.data;

      localStorage.setItem("access_token", access_token);
      localStorage.setItem("user_data", JSON.stringify(user));
      api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;

      setUser(user);

      if (user.farms?.length > 0) {
        const firstFarm = user.farms[0];
        setCurrentFarm(firstFarm);
        localStorage.setItem("current_farm_id", firstFarm.id);
      }

      return true;
    } catch (error) {
      console.error(error.response?.data);
      throw new Error(error.response?.data?.detail || "Invalid credentials");
    }
  };

  // =============================
  // REGISTER
  // =============================
  const registerUser = async (formData) => {
    try {
      const response = await api.post("/register", formData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || "Registration failed");
    }
  };

  // =============================
  // LOGOUT
  // =============================
  const logoutUser = () => {
    localStorage.clear();
    setUser(null);
    setCurrentFarm(null);
    delete api.defaults.headers.common["Authorization"];
  };

  // =============================
  // SWITCH FARM
  // =============================
  const switchFarm = (farmId) => {
    if (!user?.farms) return;
    const farm = user.farms.find((f) => f.id === Number(farmId));
    if (!farm) return;
    setCurrentFarm(farm);
    localStorage.setItem("current_farm_id", farm.id);
  };

  // =============================
  // LOAD USER ON REFRESH
  // =============================
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const storedUser = localStorage.getItem("user_data");
    const storedFarmId = localStorage.getItem("current_farm_id");

    if (token && storedUser) {
      const parsedUser = JSON.parse(storedUser);
      setUser(parsedUser);
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      if (storedFarmId && parsedUser.farms?.length > 0) {
        const farm = parsedUser.farms.find(
          (f) => f.id === Number(storedFarmId)
        );
        setCurrentFarm(farm || null);
      }
    }
  }, []);

  return (
    <UsersContext.Provider
      value={{
        user,
        currentFarm,
        loginUser,
        registerUser,
        logoutUser,
        switchFarm,
        refreshFarms,
        updateFarm, // <-- ultra-clean farm update
      }}
    >
      {children}
    </UsersContext.Provider>
  );
};

export { UsersContext, UsersProvider };