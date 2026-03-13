// src/pages/CreateFarm.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import AddFarmMembers from "../components/Farms/AddFarmMembers";

const PRODUCTION_MODULES = ["crop", "livestock", "poultry", "aquaculture"];

export default function CreateFarm() {
  const navigate = useNavigate();

  const [farmData, setFarmData] = useState({
    name: "",
    location: "",
    size: "",
    latitude: "",
    longitude: "",
  });

  const [selectedModules, setSelectedModules] = useState([]);
  const [createdFarm, setCreatedFarm] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFarmData((prev) => ({ ...prev, [name]: value }));
  };

  const toggleModule = (module) => {
    if (selectedModules.includes(module)) {
      setSelectedModules(selectedModules.filter((m) => m !== module));
    } else {
      setSelectedModules([...selectedModules, module]);
    }
  };

  const handleCreateFarm = async (e) => {
    e.preventDefault();
    setError("");

    if (selectedModules.length === 0) {
      setError("Select at least one production module");
      return;
    }

    try {
      setLoading(true);

      const payload = {
        ...farmData,
        latitude: farmData.latitude ? parseFloat(farmData.latitude) : null,
        longitude: farmData.longitude ? parseFloat(farmData.longitude) : null,
        active_modules: selectedModules, // send only modules
      };

      const res = await api.post("/farms", payload);
      setCreatedFarm(res.data);

      localStorage.setItem("current_farm_id", res.data.id);
      localStorage.setItem("farm_name", res.data.name);

    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to create farm");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto" }}>
      <h1>Create New Farm</h1>

      {!createdFarm && (
        <form onSubmit={handleCreateFarm}>
          {error && <p style={{ color: "red" }}>{error}</p>}

          <input
            type="text"
            name="name"
            placeholder="Farm Name"
            value={farmData.name}
            onChange={handleChange}
            required
          />

          <input
            type="text"
            name="location"
            placeholder="Location"
            value={farmData.location}
            onChange={handleChange}
            required
          />

          <input
            type="text"
            name="size"
            placeholder="Size (e.g., 10 hectares)"
            value={farmData.size}
            onChange={handleChange}
            required
          />

          <input
            type="number"
            name="latitude"
            placeholder="Latitude (optional)"
            value={farmData.latitude}
            onChange={handleChange}
          />

          <input
            type="number"
            name="longitude"
            placeholder="Longitude (optional)"
            value={farmData.longitude}
            onChange={handleChange}
          />

          <h3>Select Production Modules</h3>
          {PRODUCTION_MODULES.map((module) => (
            <div key={module}>
              <input
                type="checkbox"
                checked={selectedModules.includes(module)}
                onChange={() => toggleModule(module)}
              />
              <label>{module}</label>
            </div>
          ))}

          <button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Create Farm"}
          </button>
        </form>
      )}

      {createdFarm && (
        <>
          <h2>Farm Created Successfully ✅</h2>
          <p><strong>Name:</strong> {createdFarm.name}</p>
          <p><strong>Location:</strong> {createdFarm.location}</p>

          <AddFarmMembers farmId={createdFarm.id} />

          <br />

          <button onClick={() => navigate(`/farms/${createdFarm.id}`)}>
            Go to Farm Dashboard
          </button>
        </>
      )}
    </div>
  );
}
