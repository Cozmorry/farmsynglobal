import React, { useState } from "react";
import { createFinanceEntry } from "../api/financeApi";
import { useNavigate } from "react-router-dom";

export default function NewFinanceEntry() {
  const [form, setForm] = useState({
    farm_id: "",
    module_type: "",
    amount: "",
    description: "",
    entry_type: "income", // income or expense
    date: ""
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await createFinanceEntry(form);
      navigate("/finance/entries");
    } catch (err) {
      console.error(err);
      setError("Failed to create finance entry.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>New Finance Entry</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>

        <div>
          <label>Farm ID:</label>
          <input name="farm_id" value={form.farm_id} onChange={handleChange} required />
        </div>

        <div>
          <label>Module Type:</label>
          <select name="module_type" value={form.module_type} onChange={handleChange}>
            <option value="">General</option>
            <option value="poultry">Poultry</option>
            <option value="livestock">Livestock</option>
            <option value="aquaculture">Aquaculture</option>
            <option value="crop">Crop</option>
            <option value="store">Store</option>
            <option value="hr">HR</option>
          </select>
        </div>

        <div>
          <label>Entry Type:</label>
          <select name="entry_type" value={form.entry_type} onChange={handleChange}>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
        </div>

        <div>
          <label>Amount:</label>
          <input type="number" name="amount" value={form.amount} onChange={handleChange} />
        </div>

        <div>
          <label>Description:</label>
          <textarea name="description" value={form.description} onChange={handleChange} />
        </div>

        <div>
          <label>Date:</label>
          <input type="date" name="date" value={form.date} onChange={handleChange} />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save Entry"}
        </button>
      </form>
    </div>
  );
}
