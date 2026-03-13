// src/components/aquaculture/NewProduction.jsx
import React, { useState, useEffect } from "react";
import { createProduction, getPonds } from "../api/aquacultureApi";
import { useNavigate, useSearchParams } from "react-router-dom";

export default function NewProduction() {
  const [ponds, setPonds] = useState([]);
  const [pond_id, setPondId] = useState("");
  const [production_type, setProductionType] = useState("");
  const [date, setDate] = useState("");
  const [quantity, setQuantity] = useState("");
  const [unit_price, setUnitPrice] = useState("");
  const [total_value, setTotalValue] = useState("");

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

    const qty = quantity ? parseFloat(quantity) : 0;
    const price = unit_price ? parseFloat(unit_price) : 0;

    try {
      await createProduction({
        pond_id,
        production_type,
        date: date || new Date().toISOString().split("T")[0],
        quantity: qty,
        unit_price: price,
        total_value: total_value ? parseFloat(total_value) : qty * price,
      });
      navigate(`/aquaculture/ponds/${pond_id}`);
    } catch (err) {
      console.error(err);
      setError("Failed to create production record.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Production Record</h2>
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
          <label>Production Type:</label>
          <input
            type="text"
            value={production_type}
            onChange={(e) => setProductionType(e.target.value)}
            placeholder="Harvest, Sale, Other..."
            required
          />
        </div>

        <div>
          <label>Date:</label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        </div>

        <div>
          <label>Quantity:</label>
          <input type="number" step="0.01" value={quantity} onChange={(e) => setQuantity(e.target.value)} required />
        </div>

        <div>
          <label>Unit Price:</label>
          <input type="number" step="0.01" value={unit_price} onChange={(e) => setUnitPrice(e.target.value)} />
        </div>

        <div>
          <label>Total Value:</label>
          <input type="number" step="0.01" value={total_value} onChange={(e) => setTotalValue(e.target.value)} />
        </div>

        <button type="submit" disabled={loading}>{loading ? "Saving..." : "Save Production"}</button>
      </form>
    </div>
  );
}
