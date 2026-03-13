// src/components/aquaculture/NewActivity.jsx
import React, { useState, useEffect } from "react";
import { createActivity, getPonds } from "../api/aquacultureApi";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function NewActivity() {
  const [ponds, setPonds] = useState([]);
  const [pond_id, setPondId] = useState("");
  const [activity_type, setActivityType] = useState("");
  const [date, setDate] = useState("");
  const [description, setDescription] = useState("");
  const [performed_by, setPerformedBy] = useState("");
  const [cost, setCost] = useState("");

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
      await createActivity({
        pond_id,
        activity_type,
        date: date || new Date().toISOString().split("T")[0],
        description,
        performed_by,
        cost: cost ? parseFloat(cost) : 0,
      });
      navigate(`/aquaculture/ponds/${pond_id}`);
    } catch (err) {
      console.error(err);
      setError("Failed to create activity.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Activity</h2>
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
          <label>Activity Type:</label>
          <input
            type="text"
            value={activity_type}
            onChange={(e) => setActivityType(e.target.value)}
            placeholder="Feeding, Cleaning, Other..."
            required
          />
        </div>

        <div>
          <label>Date:</label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        </div>

        <div>
          <label>Description:</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
        </div>

        <div>
          <label>Performed By:</label>
          <input value={performed_by} onChange={(e) => setPerformedBy(e.target.value)} />
        </div>

        <div>
          <label>Cost:</label>
          <input type="number" step="0.01" value={cost} onChange={(e) => setCost(e.target.value)} />
        </div>

        <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save Activity"}</button>
      </form>
    </div>
  );
}
