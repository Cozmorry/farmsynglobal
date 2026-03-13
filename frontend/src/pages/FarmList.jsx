//src/pages/FarmList.jsx
import { useEffect, useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function FarmList() {
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/farms")
      .then(res => setFarms(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const handleSelectFarm = (farmId) => {
    localStorage.setItem("current_farm_id", farmId);
    navigate(`/farms/${farmId}`);
  };

  if (loading) return <p>Loading farms...</p>;
  if (farms.length === 0) return <p>No farms yet.</p>;

  return (
    <div>
      <h1>Farms</h1>
      <ul>
        {farms.map(farm => (
          <li key={farm.id} style={{ marginBottom: 10 }}>
            <span>{farm.name} ({farm.location})</span>
            <button
              onClick={() => handleSelectFarm(farm.id)}
              style={{ marginLeft: 10 }}
            >
              Open
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}