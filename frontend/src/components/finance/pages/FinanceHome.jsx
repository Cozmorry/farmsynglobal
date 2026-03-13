// src/components/finance/pages/FinanceHome.jsx
import React, { useEffect, useState } from "react";
import { getFinancialSummary } from "../api/financeApi";
import { Link } from "react-router-dom";

export default function FinanceHome() {
  const [summary, setSummary] = useState({
    totalIncome: 0,
    totalExpenses: 0,
    unpaidInvoices: 0,
    cashFlow: 0
  });

  useEffect(() => {
    async function fetchSummary() {
      try {
        const response = await getFinancialSummary();
        setSummary(response.data); // assuming API returns { totalIncome, totalExpenses, unpaidInvoices, cashFlow }
      } catch (error) {
        console.error("Error fetching finance summary:", error);
      }
    }
    fetchSummary();
  }, []);

  const cards = [
    {
      title: "Total Income",
      value: summary.totalIncome,
      color: "bg-green-100",
      link: "/finance/entries"
    },
    {
      title: "Total Expenses",
      value: summary.totalExpenses,
      color: "bg-red-100",
      link: "/finance/entries"
    },
    {
      title: "Unpaid Invoices",
      value: summary.unpaidInvoices,
      color: "bg-yellow-100",
      link: "/finance/invoices"
    },
    {
      title: "Cash Flow",
      value: summary.cashFlow,
      color: "bg-blue-100",
      link: "/finance/report"
    }
  ];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Finance Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map((card) => (
          <Link key={card.title} to={card.link}>
            <div className={`p-4 rounded-lg shadow ${card.color} hover:shadow-lg transition`}>
              <h2 className="text-lg font-semibold">{card.title}</h2>
              <p className="text-2xl mt-2 font-bold">{card.value}</p>
            </div>
          </Link>
        ))}
      </div>

      <div className="mt-8 flex gap-4 flex-wrap">
        <Link
          to="/finance/invoice/new"
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
        >
          New Invoice
        </Link>
        <Link
          to="/finance/payment/new"
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          New Payment
        </Link>
        <Link
          to="/finance/report"
          className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition"
        >
          View Reports
        </Link>
      </div>
    </div>
  );
}
