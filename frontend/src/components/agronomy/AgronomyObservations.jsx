// src/components/agronomy/AgronomyObservations.jsx
import React, { useEffect, useState } from "react";
import { getObservations, createObservation } from "./api/agronomyApi";
import AgronomyFileUpload from "./AgronomyFileUpload";

const AgronomyObservations = ({ cropId, blockId }) => {
  const [observations, setObservations] = useState([]);
  const [form, setForm] = useState({ notes: "", pest_issues: "", disease_issues: "", nutrient_deficiencies: "", suggested_action: "" });
  const [loading, setLoading] = useState(false);
  const [filterDate, setFilterDate] = useState("");

  const fetchObservations = async () => {
    try {
      const res = await getObservations({ crop_id: cropId, block_id: blockId });
      setObservations(res.data);
    } catch (err) {
      console.error("Error fetching observations:", err);
    }
  };

  useEffect(() => { fetchObservations(); }, [cropId, blockId]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createObservation({ ...form, crop_id: cropId, block_id: blockId });
      setForm({ notes: "", pest_issues: "", disease_issues: "", nutrient_deficiencies: "", suggested_action: "" });
      fetchObservations();
    } catch (err) {
      console.error("Error creating observation:", err);
      alert("Creation failed.");
    } finally { setLoading(false); }
  };

  const filtered = filterDate
    ? observations.filter(o => o.created_at?.slice(0, 10) === filterDate)
    : observations;

  return (
    <div>
      <h2>Agronomy Observations</h2>

      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
        <textarea name="notes" placeholder="Notes" value={form.notes} onChange={handleChange} required />
        <input type="text" name="pest_issues" placeholder="Pest Issues" value={form.pest_issues} onChange={handleChange} />
        <input type="text" name="disease_issues" placeholder="Disease Issues" value={form.disease_issues} onChange={handleChange} />
        <input type="text" name="nutrient_deficiencies" placeholder="Nutrient Deficiencies" value={form.nutrient_deficiencies} onChange={handleChange} />
        <input type="text" name="suggested_action" placeholder="Suggested Action" value={form.suggested_action} onChange={handleChange} />
        <button type="submit" disabled={loading}>{loading ? "Creating..." : "Create Observation"}</button>
      </form>

      <label>
        Filter by date: 
        <input type="date" value={filterDate} onChange={(e) => setFilterDate(e.target.value)} />
      </label>

      <ul>
        {filtered.map((obs) => (
          <li key={obs.id}>
            <strong>{obs.notes}</strong>
            <br />
            <small>Date: {new Date(obs.created_at).toLocaleDateString()}</small>
            <AgronomyFileUpload type="observation" id={obs.id} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AgronomyObservations;



