import React, { useEffect, useState } from "react";
import { getHarvests, deleteHarvest } from "../api/aquacultureApi";
import { Link } from "react-router-dom";

export default function HarvestList({ pondId }) {
  const [records, setRecords] = useState([]);

  const fetchData = async () => {
    try {
      const res = await getHarvests({ pond_id: pondId });
      const harvestsArray = Array.isArray(res.data) ? res.data : res.data?.harvests || [];
      setRecords(harvestsArray);
    } catch (err) {
      console.error("Failed to fetch harvests:", err);
      setRecords([]);
    }
  };

  useEffect(() => {
    if (pondId) fetchData();
  }, [pondId]);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this harvest?")) {
      await deleteHarvest(id);
      fetchData();
    }
  };

  return (
    <div>
      <h3>Harvest Records</h3>
      <Link to={`/aquaculture/harvest/new?pond_id=${pondId}`}>
        <button>Add New Harvest</button>
      </Link>
      <ul>
        {records.length > 0 ? (
          records.map((h) => (
            <li key={h.id}>
              {h.date} — Total: {h.total_weight} kg — Avg: {h.average_weight} kg — Mortality: {h.mortality}
              <button onClick={() => handleDelete(h.id)} style={{ marginLeft: 10 }}>
                Delete
              </button>
            </li>
          ))
        ) : (
          <li>No harvest records found</li>
        )}
      </ul>
    </div>
  );
}
