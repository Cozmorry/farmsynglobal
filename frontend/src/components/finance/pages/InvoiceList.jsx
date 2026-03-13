// src/components/finance/pages/InvoiceList.jsx
import React, { useEffect, useState } from "react";
import { getInvoices } from "../api/financeApi";
import { Link } from "react-router-dom";

export default function InvoiceList({ farmId }) {
  const [invoices, setInvoices] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInvoices() {
      try {
        const response = await getInvoices({ farm_id: farmId });
        setInvoices(Array.isArray(response.data) ? response.data : []);
      } catch (error) {
        console.error("Error fetching invoices:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchInvoices();
  }, [farmId]);

  const filteredInvoices = invoices.filter(
    (inv) =>
      inv.customerName.toLowerCase().includes(search.toLowerCase()) ||
      inv.invoiceNumber.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Invoices</h1>
        <Link
          to="/finance/invoice/new"
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
        >
          New Invoice
        </Link>
      </div>

      <input
        type="text"
        placeholder="Search by customer or invoice number..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-4 p-2 border rounded w-full md:w-1/3"
      />

      {loading ? (
        <p>Loading invoices...</p>
      ) : filteredInvoices.length === 0 ? (
        <p>No invoices found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border rounded shadow">
            <thead>
              <tr className="bg-gray-100">
                <th className="py-2 px-4 border-b">Invoice #</th>
                <th className="py-2 px-4 border-b">Customer</th>
                <th className="py-2 px-4 border-b">Amount</th>
                <th className="py-2 px-4 border-b">Status</th>
                <th className="py-2 px-4 border-b">Date</th>
                <th className="py-2 px-4 border-b">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredInvoices.map((invoice) => (
                <tr key={invoice.id} className="hover:bg-gray-50">
                  <td className="py-2 px-4 border-b">{invoice.invoiceNumber}</td>
                  <td className="py-2 px-4 border-b">{invoice.customerName}</td>
                  <td className="py-2 px-4 border-b">${invoice.amount.toFixed(2)}</td>
                  <td className="py-2 px-4 border-b">
                    <span
                      className={`px-2 py-1 rounded-full text-sm ${
                        invoice.status === "Paid"
                          ? "bg-green-100 text-green-800"
                          : invoice.status === "Pending"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {invoice.status}
                    </span>
                  </td>
                  <td className="py-2 px-4 border-b">
                    {new Date(invoice.date).toLocaleDateString()}
                  </td>
                  <td className="py-2 px-4 border-b flex gap-2">
                    <Link
                      to={`/finance/invoice/${invoice.id}`}
                      className="px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition text-sm"
                    >
                      View
                    </Link>
                    <button
                      className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition text-sm"
                      onClick={() => alert("Delete feature coming soon!")}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
