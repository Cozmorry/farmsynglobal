import React, { useEffect, useState } from "react";
import { getFeedings, deleteFeeding } from "../api/aquacultureApi";
import { Link } from "react-router-dom";

export default function FeedingList({ pondId }) {
  const [feedings, setFeedings] = useState([]);

  const fetchData = async () => {
    try {
      const res = await getFeedings({ pond_id: pondId });
      const feedingsArray = Array.isArray(res.data) ? res.data : res.data?.feedings || [];
      setFeedings(feedingsArray);
    } catch (err) {
      console.error("Failed to fetch feedings:", err);
      setFeedings([]);
    }
  };

  useEffect(() => {
    if (pondId) fetchData();
  }, [pondId]);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this feeding?")) {
      await deleteFeeding(id);
      fetchData();
    }
  };

  return (
    <div>
      <h3>Feedings</h3>
      <Link to={`/aquaculture/feedings/new?pond_id=${pondId}`}>
        <button>Add New Feeding</button>
      </Link>
      <ul>
        {feedings.length > 0 ? (
          feedings.map((f) => (
            <li key={f.id}>
              {f.date} — {f.feed_quantity} kg — {f.feed_type}
              <button onClick={() => handleDelete(f.id)} style={{ marginLeft: 10 }}>
                Delete
              </button>
            </li>
          ))
        ) : (
          <li>No feedings found</li>
        )}
      </ul>
    </div>
  );
}
