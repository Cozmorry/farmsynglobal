// src/components/aquaculture/forms/NewWaterQuality.jsx
import React, { useState, useEffect } from "react";
import { createWaterRecord, getPonds } from "../api/aquacultureApi";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function NewWaterQuality() {
  const [ponds, setPonds] = useState([]);
  const [pond_id, setPondId] = useState("");
  const [date, setDate] = useState("");
  const [temperature, setTemperature] = useState("");
  const [ph_level, setPhLevel] = useState("");
  const [dissolved_oxygen, setDissolvedOxygen] = useState("");
  const [ammonia, setAmmonia] = useState("");
  const [turbidity, setTurbidity] = useState("");
  const [notes, setNotes] = useState("");

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
      await createWaterRecord({
        pond_id,
        date: date || new Date().toISOString().split("T")[0],
        temperature: temperature ? parseFloat(temperature) : null,
        ph_level: ph_level ? parseFloat(ph_level) : null,
        dissolved_oxygen: dissolved_oxygen ? parseFloat(dissolved_oxygen) : null,
        ammonia: ammonia ? parseFloat(ammonia) : null,
        turbidity: turbidity ? parseFloat(turbidity) : null,
        notes,
      });
      navigate(`/aquaculture/ponds/${pond_id}`);
    } catch (err) {
      console.error(err);
      setError("Failed to create water quality record.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Water Quality Record</h2>
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
          <label>Temperature (°C):</label>
          <input type="number" step="0.1" value={temperature} onChange={(e) => setTemperature(e.target.value)} />
        </div>

        <div>
          <label>pH Level:</label>
          <input type="number" step="0.01" value={ph_level} onChange={(e) => setPhLevel(e.target.value)} />
        </div>

        <div>
          <label>Dissolved Oxygen (mg/L):</label>
          <input type="number" step="0.01" value={dissolved_oxygen} onChange={(e) => setDissolvedOxygen(e.target.value)} />
        </div>

        <div>
          <label>Ammonia (mg/L):</label>
          <input type="number" step="0.01" value={ammonia} onChange={(e) => setAmmonia(e.target.value)} />
        </div>

        <div>
          <label>Turbidity:</label>
          <input type="number" step="0.01" value={turbidity} onChange={(e) => setTurbidity(e.target.value)} />
        </div>

        <div>
          <label>Notes:</label>
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)} />
        </div>

        <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save Water Record"}</button>
      </form>
    </div>
  );
}
