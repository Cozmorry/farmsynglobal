// src/components/finance/forms/NewInvoice.jsx
import React, { useState } from "react";
import { createInvoice } from "../api/financeApi";
import { useNavigate } from "react-router-dom";

export default function NewInvoice() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    invoiceNumber: "",
    customerName: "",
    amount: "",
    status: "Pending",
    date: new Date().toISOString().slice(0, 10), // default to today
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Basic validation
    if (!formData.invoiceNumber || !formData.customerName || !formData.amount) {
      setError("Please fill in all required fields.");
      return;
    }

    setLoading(true);
    try {
      await createInvoice({
        ...formData,
        amount: parseFloat(formData.amount),
      });
      navigate("/finance/invoices"); // redirect to invoice list
    } catch (err) {
      console.error(err);
      setError("Failed to create invoice. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-6">New Invoice</h1>

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
          <label className="block mb-1 font-medium">Customer Name *</label>
          <input
            type="text"
            name="customerName"
            value={formData.customerName}
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
          <label className="block mb-1 font-medium">Status</label>
          <select
            name="status"
            value={formData.status}
            onChange={handleChange}
            className="w-full border rounded p-2"
          >
            <option value="Pending">Pending</option>
            <option value="Paid">Paid</option>
            <option value="Overdue">Overdue</option>
          </select>
        </div>

        <div>
          <label className="block mb-1 font-medium">Invoice Date</label>
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            className="w-full border rounded p-2"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 px-4 rounded text-white ${
            loading ? "bg-gray-400" : "bg-green-500 hover:bg-green-600"
          } transition`}
        >
          {loading ? "Saving..." : "Create Invoice"}
        </button>
      </form>
    </div>
  );
}
