import React, { useEffect, useState } from "react";
import { getWaterRecords, deleteWaterRecord } from "../api/aquacultureApi";
import { Link } from "react-router-dom";

export default function WaterQualityList({ pondId }) {
  const [records, setRecords] = useState([]);

  const fetchData = async () => {
    try {
      const res = await getWaterRecords({ pond_id: pondId });
      const waterArray = Array.isArray(res.data) ? res.data : res.data?.water_records || [];
      setRecords(waterArray);
    } catch (err) {
      console.error("Failed to fetch water records:", err);
      setRecords([]);
    }
  };

  useEffect(() => {
    if (pondId) fetchData();
  }, [pondId]);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this record?")) {
      await deleteWaterRecord(id);
      fetchData();
    }
  };

  return (
    <div>
      <h3>Water Quality Records</h3>
      <Link to={`/aquaculture/water_quality/new?pond_id=${pondId}`}>
        <button>Add New Water Record</button>
      </Link>
      <ul>
        {records.length > 0 ? (
          records.map((r) => (
            <li key={r.id}>
              {r.date} — Temp: {r.temperature}°C — pH: {r.ph_level} — DO: {r.dissolved_oxygen} mg/L
              <button onClick={() => handleDelete(r.id)} style={{ marginLeft: 10 }}>
                Delete
              </button>
            </li>
          ))
        ) : (
          <li>No water quality records found</li>
        )}
      </ul>
    </div>
  );
}
