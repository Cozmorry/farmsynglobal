// src/components/aquaculture/NewHarvest.jsx
import React, { useState, useEffect } from "react";
import { createHarvest, getPonds } from "../api/aquacultureApi";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function NewHarvest() {
  const [ponds, setPonds] = useState([]);
  const [pond_id, setPondId] = useState("");
  const [date, setDate] = useState("");
  const [total_weight, setTotalWeight] = useState("");
  const [average_weight, setAverageWeight] = useState("");
  const [mortality, setMortality] = useState("");
  const [remarks, setRemarks] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const fetchPonds = async () => {
      const res = await getPonds();
      setPonds(res.data || []);
    };
    fetchPonds();
  }, []);

  useEffect(() => {
    const pondIdFromUrl = searchParams.get("pond_id");
    if (pondIdFromUrl) setPondId(pondIdFromUrl);
  }, [searchParams]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await createHarvest({
        pond_id,
        date: date || new Date().toISOString().split("T")[0],
        total_weight: total_weight ? parseFloat(total_weight) : 0,
        average_weight: average_weight ? parseFloat(average_weight) : null,
        mortality: mortality ? parseInt(mortality) : 0,
        remarks,
      });
      navigate(`/aquaculture/ponds/${pond_id}`);
    } catch (err) {
      console.error(err);
      setError("Failed to create harvest record.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Harvest Record</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Pond:</label>
          <select value={pond_id} onChange={(e) => setPondId(e.target.value)} required>
            <option value="">Select Pond</option>
            {ponds.map((p) => (
              <option key={p.id} value={p.id}>{p.pond_name}</option>
            ))}
          </select>
        </div>

        <div>
          <label>Date:</label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        </div>

        <div>
          <label>Total Weight (kg):</label>
          <input type="number" step="0.01" value={total_weight} onChange={(e) => setTotalWeight(e.target.value)} required />
        </div>

        <div>
          <label>Average Weight (kg):</label>
          <input type="number" step="0.01" value={average_weight} onChange={(e) => setAverageWeight(e.target.value)} />
        </div>

        <div>
          <label>Mortality:</label>
          <input type="number" value={mortality} onChange={(e) => setMortality(e.target.value)} />
        </div>

        <div>
          <label>Remarks:</label>
          <textarea value={remarks} onChange={(e) => setRemarks(e.target.value)} />
        </div>

        <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save Harvest Record"}</button>
      </form>
    </div>
  );
}
