import React, { useEffect, useState } from "react";
import { getRecommendations, deleteRecommendation } from "../api/aquacultureApi";
import { Link } from "react-router-dom";

export default function RecommendationList({ healthId }) {
  const [records, setRecords] = useState([]);

  const fetchData = async () => {
    try {
      const res = await getRecommendations({ health_id: healthId });
      const recArray = Array.isArray(res.data) ? res.data : res.data?.recommendations || [];
      setRecords(recArray);
    } catch (err) {
      console.error("Failed to fetch recommendations:", err);
      setRecords([]);
    }
  };

  useEffect(() => {
    if (healthId) fetchData();
  }, [healthId]);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this recommendation?")) {
      await deleteRecommendation(id);
      fetchData();
    }
  };

  return (
    <div>
      <h3>Veterinary Recommendations</h3>
      <Link to={`/aquaculture/recommendation/new?health_id=${healthId}`}>
        <button>Add New Recommendation</button>
      </Link>
      <ul>
        {records.length > 0 ? (
          records.map((r) => (
            <li key={r.id}>
              {r.date} — {r.recommendation}
              <button onClick={() => handleDelete(r.id)} style={{ marginLeft: 10 }}>
                Delete
              </button>
            </li>
          ))
        ) : (
          <li>No recommendations found</li>
        )}
      </ul>
    </div>
  );
}
