import React, { useEffect, useState } from "react";
import { getPonds, deletePond } from "../api/aquacultureApi";
import { Link } from "react-router-dom";

export default function PondList() {
  const [ponds, setPonds] = useState([]);

  const fetchData = async () => {
    try {
      const res = await getPonds();
      const pondsArray = Array.isArray(res.data) ? res.data : res.data?.ponds || [];
      setPonds(pondsArray);
    } catch (err) {
      console.error("Failed to fetch ponds:", err);
      setPonds([]);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this pond?")) {
      await deletePond(id);
      fetchData();
    }
  };

  return (
    <div>
      <h2>Ponds</h2>
      <Link to="/aquaculture/ponds/new">
        <button>Add New Pond</button>
      </Link>
      <ul>
        {ponds.length > 0 ? (
          ponds.map((p) => (
            <li key={p.id}>
              {p.pond_name} — {p.species} — {p.pond_size} m² — Stock: {p.stock_quantity}
              <button onClick={() => handleDelete(p.id)} style={{ marginLeft: 10 }}>
                Delete
              </button>
            </li>
          ))
        ) : (
          <li>No ponds found</li>
        )}
      </ul>
    </div>
  );
}
