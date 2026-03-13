// src/components/finance/forms/NewPayment.jsx
import React, { useState } from "react";
import { createPayment } from "../api/financeApi";
import { useNavigate } from "react-router-dom";

export default function NewPayment() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    invoiceNumber: "",
    amount: "",
    paymentDate: new Date().toISOString().slice(0, 10),
    method: "Cash",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!formData.invoiceNumber || !formData.amount) {
      setError("Invoice number and amount are required.");
      return;
    }

    setLoading(true);
    try {
      await createPayment({
        ...formData,
        amount: parseFloat(formData.amount),
      });
      navigate("/finance/payments");
    } catch (err) {
      console.error(err);
      setError("Failed to create payment. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-6">New Payment</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Invoice Number *</label>
          <input
            type="text"
            name="invoiceNumber"
            value={formData.invoiceNumber}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block mb-1 font-medium">Amount ($) *</label>
          <input
            type="number"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            className="w-full border rounded p-2"
            min="0"
            step="0.01"
          />
        </div>

        <div>
          <label className="block mb-1 font-medium">Payment Date</label>
          <input
            type="date"
            name="paymentDate"
            value={formData.paymentDate}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block mb-1 font-medium">Payment Method</label>
          <select
            name="method"
            value={formData.method}
            onChange={handleChange}
            className="w-full border rounded p-2"
          >
            <option value="Cash">Cash</option>
            <option value="Card">Card</option>
            <option value="Bank Transfer">Bank Transfer</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 px-4 rounded text-white ${
            loading ? "bg-gray-400" : "bg-green-500 hover:bg-green-600"
          } transition`}
        >
          {loading ? "Saving..." : "Create Payment"}
        </button>
      </form>
    </div>
  );
}
