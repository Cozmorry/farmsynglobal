// src/components/aquaculture/NewRecommendation.jsx
import React, { useState, useEffect } from "react";
import { createRecommendation, getHealth } from "../api/aquacultureApi";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function NewRecommendation() {
  const [healthRecords, setHealthRecords] = useState([]);
  const [health_id, setHealthId] = useState("");
  const [recommendation, setRecommendation] = useState("");
  const [date, setDate] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await getHealthRecords();
        setHealthRecords(res.data || []);
      } catch (err) {
        console.error(err);
        setError("Failed to load health records.");
      }
    };
    fetchHealth();
  }, []);

  useEffect(() => {
    const healthIdFromUrl = searchParams.get("health_id");
    if (healthIdFromUrl) setHealthId(healthIdFromUrl);
  }, [searchParams]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await createRecommendation({
        health_id,
        recommendation,
        date: date || new Date().toISOString().split("T")[0],
      });
      navigate(`/aquaculture/health/${health_id}`);
    } catch (err) {
      console.error(err);
      setError("Failed to create recommendation.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Veterinary Recommendation</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Health Record:</label>
          <select
            value={health_id}
            onChange={(e) => setHealthId(e.target.value)}
            required
          >
            <option value="">Select Health Record</option>
            {healthRecords.map((h) => (
              <option key={h.id} value={h.id}>
                {h.date} — {h.disease}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Recommendation:</label>
          <textarea
            value={recommendation}
            onChange={(e) => setRecommendation(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Date:</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save Recommendation"}
        </button>
      </form>
    </div>
  );
}
