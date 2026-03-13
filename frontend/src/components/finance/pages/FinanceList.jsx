import React, { useEffect, useState } from "react";
import { getFinancialSummary } from "../api/financeApi";
import { Link } from "react-router-dom";

export default function FinanceList() {
  const [summary, setSummary] = useState(null);

  const fetchData = async () => {
    try {
      const res = await getFinancialSummary({ farm_id: 1 }); // use real farm id
      setSummary(res.data);
    } catch (err) {
      console.error("Failed to load finance summary:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (!summary) return <p>Loading...</p>;

  return (
    <div>
      <h2>Finance Summary</h2>

      <Link to="/finance/entry/new">
        <button>Add Finance Entry</button>
      </Link>

      <ul>
        <li>Total Income: {summary.total_income}</li>
        <li>Total Expenses: {summary.total_expenses}</li>
        <li>Profit: {summary.net_profit}</li>
      </ul>
    </div>
  );
}
