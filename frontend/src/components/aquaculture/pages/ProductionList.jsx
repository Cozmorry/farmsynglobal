import React, { useEffect, useState } from "react";
import { getProductions, deleteProduction } from "../api/aquacultureApi";
import { Link } from "react-router-dom";

export default function ProductionList({ pondId }) {
  const [records, setRecords] = useState([]);

  const fetchData = async () => {
    try {
      const res = await getProductions({ pond_id: pondId });
      const prodArray = Array.isArray(res.data) ? res.data : res.data?.productions || [];
      setRecords(prodArray);
    } catch (err) {
      console.error("Failed to fetch production records:", err);
      setRecords([]);
    }
  };

  useEffect(() => {
    if (pondId) fetchData();
  }, [pondId]);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this production record?")) {
      await deleteProduction(id);
      fetchData();
    }
  };

  return (
    <div>
      <h3>Production Records</h3>
      <Link to={`/aquaculture/production/new?pond_id=${pondId}`}>
        <button>Add New Production</button>
      </Link>
      <ul>
        {records.length > 0 ? (
          records.map((r) => (
            <li key={r.id}>
              {r.date} — {r.production_type} — Qty: {r.quantity} — Price: {r.unit_price} — Total: {r.total_value}
              <button onClick={() => handleDelete(r.id)} style={{ marginLeft: 10 }}>
                Delete
              </button>
            </li>
          ))
        ) : (
          <li>No production records found</li>
        )}
      </ul>
    </div>
  );
}
