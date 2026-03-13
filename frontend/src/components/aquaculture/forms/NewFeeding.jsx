// src/components/aquaculture/NewFeeding.jsx
import React, { useState, useEffect } from "react";
import { createFeeding, getPonds } from "../api/aquacultureApi";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function NewFeeding() {
  const [ponds, setPonds] = useState([]);
  const [pond_id, setPondId] = useState("");
  const [date, setDate] = useState("");
  const [feed_quantity, setFeedQuantity] = useState("");
  const [feed_type, setFeedType] = useState("");
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
      await createFeeding({
        pond_id,
        date: date || new Date().toISOString().split("T")[0],
        feed_quantity: parseFloat(feed_quantity),
        feed_type,
        remarks,
      });
      navigate(`/aquaculture/ponds/${pond_id}`);
    } catch (err) {
      console.error(err);
      setError("Failed to create feeding record.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Feeding</h2>
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
          <label>Feed Quantity (kg):</label>
          <input type="number" step="0.01" value={feed_quantity} onChange={(e) => setFeedQuantity(e.target.value)} required />
        </div>

        <div>
          <label>Feed Type:</label>
          <input value={feed_type} onChange={(e) => setFeedType(e.target.value)} />
        </div>

        <div>
          <label>Remarks:</label>
          <textarea value={remarks} onChange={(e) => setRemarks(e.target.value)} />
        </div>

        <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save Feeding"}</button>
      </form>
    </div>
  );
}
