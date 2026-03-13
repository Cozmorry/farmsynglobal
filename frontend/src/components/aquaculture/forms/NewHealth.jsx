// src/components/aquaculture/NewHealth.jsx
import React, { useState, useEffect } from "react";
import { createHealth, getPonds } from "../api/aquacultureApi";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function NewHealth() {
  const [ponds, setPonds] = useState([]);
  const [pond_id, setPondId] = useState("");
  const [date, setDate] = useState("");
  const [disease, setDisease] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [treatment, setTreatment] = useState("");
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
      await createHealth({
        pond_id,
        date: date || new Date().toISOString().split("T")[0],
        disease,
        symptoms,
        treatment,
        remarks,
      });
      navigate(`/aquaculture/ponds/${pond_id}`);
    } catch (err) {
      console.error(err);
      setError("Failed to create health record.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Health Record</h2>
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
          <label>Disease:</label>
          <input type="text" value={disease} onChange={(e) => setDisease(e.target.value)} required />
        </div>

        <div>
          <label>Symptoms:</label>
          <textarea value={symptoms} onChange={(e) => setSymptoms(e.target.value)} />
        </div>

        <div>
          <label>Treatment:</label>
          <textarea value={treatment} onChange={(e) => setTreatment(e.target.value)} />
        </div>

        <div>
          <label>Remarks:</label>
          <textarea value={remarks} onChange={(e) => setRemarks(e.target.value)} />
        </div>

        <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save Health Record"}</button>
      </form>
    </div>
  );
}
