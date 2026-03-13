// src/components/aquaculture/NewPond.jsx
import React, { useState } from "react";
import { createPond } from "../api/aquacultureApi";
import { useNavigate } from "react-router-dom";

export default function NewPond() {
  const [pond_name, setPondName] = useState("");
  const [species, setSpecies] = useState("");
  const [pond_size, setPondSize] = useState("");
  const [stock_quantity, setStockQuantity] = useState("");
  const [average_weight, setAverageWeight] = useState("");
  const [feed_type, setFeedType] = useState("");
  const [feed_cost, setFeedCost] = useState("");
  const [water_quality_status, setWaterQuality] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await createPond({
        pond_name,
        species,
        pond_size: pond_size ? parseFloat(pond_size) : null,
        stock_quantity: stock_quantity ? parseInt(stock_quantity) : null,
        average_weight: average_weight ? parseFloat(average_weight) : 0,
        feed_type,
        feed_cost: feed_cost ? parseFloat(feed_cost) : null,
        water_quality_status,
      });
      navigate("/aquaculture/ponds");
    } catch (err) {
      console.error(err);
      setError("Failed to create pond.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Pond</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Pond Name:</label>
          <input value={pond_name} onChange={(e) => setPondName(e.target.value)} required />
        </div>

        <div>
          <label>Species:</label>
          <input value={species} onChange={(e) => setSpecies(e.target.value)} required />
        </div>

        <div>
          <label>Pond Size (m²):</label>
          <input type="number" step="0.01" value={pond_size} onChange={(e) => setPondSize(e.target.value)} />
        </div>

        <div>
          <label>Stock Quantity:</label>
          <input type="number" value={stock_quantity} onChange={(e) => setStockQuantity(e.target.value)} />
        </div>

        <div>
          <label>Average Weight (kg):</label>
          <input type="number" step="0.01" value={average_weight} onChange={(e) => setAverageWeight(e.target.value)} />
        </div>

        <div>
          <label>Feed Type:</label>
          <input value={feed_type} onChange={(e) => setFeedType(e.target.value)} />
        </div>

        <div>
          <label>Feed Cost:</label>
          <input type="number" step="0.01" value={feed_cost} onChange={(e) => setFeedCost(e.target.value)} />
        </div>

        <div>
          <label>Water Quality Status:</label>
          <input value={water_quality_status} onChange={(e) => setWaterQuality(e.target.value)} />
        </div>

        <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save Pond"}</button>
      </form>
    </div>
  );
}
