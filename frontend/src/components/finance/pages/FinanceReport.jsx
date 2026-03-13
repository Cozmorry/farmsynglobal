import React, { useState, useEffect } from "react";
import { getFinancialSummary, exportFinanceTable } from "../api/financeApi";

export default function FinanceReport({ farmId }) {
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchSummary() {
      try {
        const response = await getFinancialSummary({ farm_id: farmId });
        // Ensure it's an array
        setSummary(Array.isArray(response.data) ? response.data : []);
      } catch (err) {
        console.error(err);
        setError("Failed to load financial summary.");
      } finally {
        setLoading(false);
      }
    }
    fetchSummary();
  }, [farmId]);

  const handleExport = async (format = "excel") => {
    try {
      const blob = await exportFinanceTable("summary", { farm_id: farmId, format });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `financial_summary.${format === "pdf" ? "pdf" : "xlsx"}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
      alert("Failed to export. Try again.");
    }
  };

  if (loading) return <p className="p-6">Loading summary...</p>;
  if (error) return <p className="p-6 text-red-500">{error}</p>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Finance Summary Report</h1>
        <div className="space-x-2">
          <button
            onClick={() => handleExport("excel")}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Export Excel
          </button>
          <button
            onClick={() => handleExport("pdf")}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Export PDF
          </button>
        </div>
      </div>

      {summary.length === 0 ? (
        <p>No data available.</p>
      ) : (
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2">Category</th>
              <th className="border p-2">Total Income</th>
              <th className="border p-2">Total Expense</th>
              <th className="border p-2">Profit</th>
            </tr>
          </thead>
          <tbody>
            {summary.map((item, idx) => (
              <tr key={idx} className="hover:bg-gray-50">
                <td className="border p-2">{item.category || "General"}</td>
                <td className="border p-2">${item.total_income.toFixed(2)}</td>
                <td className="border p-2">${item.total_expense.toFixed(2)}</td>
                <td className="border p-2">${item.profit.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
