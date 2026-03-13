import React, { useEffect, useState } from "react";
import { getHealth, deleteHealth } from "../api/aquacultureApi";
import { Link } from "react-router-dom";

export default function HealthList({ pondId }) {
  const [records, setRecords] = useState([]);

  const fetchData = async () => {
    try {
      const res = await getHealth({ pond_id: pondId });
      const healthArray = Array.isArray(res.data) ? res.data : res.data?.health_records || [];
      setRecords(healthArray);
    } catch (err) {
      console.error("Failed to fetch health records:", err);
      setRecords([]);
    }
  };

  useEffect(() => {
    if (pondId) fetchData();
  }, [pondId]);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this health record?")) {
      await deleteHealth(id);
      fetchData();
    }
  };

  return (
    <div>
      <h3>Health Records</h3>
      <Link to={`/aquaculture/health/new?pond_id=${pondId}`}>
        <button>Add New Health Record</button>
      </Link>
      <ul>
        {records.length > 0 ? (
          records.map((r) => (
            <li key={r.id}>
              {r.date} — Disease: {r.disease} — Symptoms: {r.symptoms} — Treatment: {r.treatment}
              <button onClick={() => handleDelete(r.id)} style={{ marginLeft: 10 }}>
                Delete
              </button>
            </li>
          ))
        ) : (
          <li>No health records found</li>
        )}
      </ul>
    </div>
  );
}
