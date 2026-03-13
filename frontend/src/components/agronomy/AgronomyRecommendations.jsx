// src/components/agronomy/AgronomyRecommendations.jsx
import React, { useEffect, useState } from "react";
import { getRecommendations, createRecommendation } from "./api/agronomyApi";
import AgronomyFileUpload from "./AgronomyFileUpload";

const AgronomyRecommendations = ({ cropId, blockId }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [form, setForm] = useState({ recommendation_text: "", recommended_action: "", source: "" });
  const [loading, setLoading] = useState(false);
  const [filterDate, setFilterDate] = useState("");

  const fetchRecommendations = async () => {
    try {
      const res = await getRecommendations({ crop_id: cropId, block_id: blockId });
      setRecommendations(res.data);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
    }
  };

  useEffect(() => { fetchRecommendations(); }, [cropId, blockId]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createRecommendation({ ...form, crop_id: cropId, block_id: blockId });
      setForm({ recommendation_text: "", recommended_action: "", source: "" });
      fetchRecommendations();
    } catch (err) {
      console.error("Error creating recommendation:", err);
      alert("Creation failed.");
    } finally { setLoading(false); }
  };

  // Filter by date
  const filtered = filterDate
    ? recommendations.filter(r => r.created_at?.slice(0, 10) === filterDate)
    : recommendations;

  return (
    <div>
      <h2>Agronomy Recommendations</h2>

      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
        <input type="text" name="recommendation_text" placeholder="Recommendation" value={form.recommendation_text} onChange={handleChange} required />
        <input type="text" name="recommended_action" placeholder="Recommended Action" value={form.recommended_action} onChange={handleChange} />
        <input type="text" name="source" placeholder="Source" value={form.source} onChange={handleChange} />
        <button type="submit" disabled={loading}>{loading ? "Creating..." : "Create Recommendation"}</button>
      </form>

      <label>
        Filter by date: 
        <input type="date" value={filterDate} onChange={(e) => setFilterDate(e.target.value)} />
      </label>

      <ul>
        {filtered.map((rec) => (
          <li key={rec.id}>
            <strong>{rec.recommendation_text}</strong> - {rec.recommended_action || "N/A"}  
            <br />
            <small>Source: {rec.source || "N/A"} | Date: {new Date(rec.created_at).toLocaleDateString()}</small>
            <AgronomyFileUpload type="recommendation" id={rec.id} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AgronomyRecommendations;


