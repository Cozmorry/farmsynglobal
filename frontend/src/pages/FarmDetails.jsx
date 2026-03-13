// src/pages/FarmDetails.jsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";
import "./Home.css";

import UnitToggle from "../components/UnitToggle";
import StructureCard from "../components/Farms/StructureCard";

export default function FarmDetails() {
  const { farmId } = useParams();

  const [farm, setFarm] = useState(null);
  const [loading, setLoading] = useState(true);

  const [structures, setStructures] = useState({
    blocks: [],
    greenhouses: [],
    barns: [],
    coops: [],
    ponds: [],
  });

  const [newStructure, setNewStructure] = useState({
    type: "",
    name: "",
    area: "",
    capacity: "",
  });

  const [unit, setUnit] = useState("ha"); // hectare / acre toggle

  // ------------------------------------------------
  // FETCH DATA
  // ------------------------------------------------
  useEffect(() => {
    if (!farmId) return;

    const fetchData = async () => {
      try {
        setLoading(true);

        const farmRes = await api.get(`/farms/${farmId}`);
        setFarm(farmRes.data);

        const structRes = await api.get(`/farms/workspace/structures`, {
          headers: { "X-Farm-ID": farmId },
        });

        setStructures(structRes.data);
      } catch (err) {
        console.error("Error loading farm:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [farmId]);

  if (loading) return <p>Loading farm...</p>;
  if (!farm) return <p>Farm not found.</p>;

  // ------------------------------------------------
  // MODULE → STRUCTURES MAP
  // ------------------------------------------------
  const moduleMap = {
    crop: ["block", "greenhouse"],
    livestock: ["barn"],
    poultry: ["coop"],
    aquaculture: ["pond"],
  };

  let availableTypes = [];
  farm.active_modules?.forEach((m) => {
    if (moduleMap[m]) availableTypes = [...availableTypes, ...moduleMap[m]];
  });
  availableTypes = [...new Set(availableTypes)];

  // ------------------------------------------------
  // ADD STRUCTURE
  // ------------------------------------------------
  const handleAddStructure = async () => {
    if (!newStructure.type || !newStructure.name) {
      alert("Select structure type and name");
      return;
    }

    const payload = { name: newStructure.name };

    if (["block", "greenhouse", "pond"].includes(newStructure.type)) {
      payload.area = newStructure.area ? Number(newStructure.area) : null;
    }

    if (["barn", "coop"].includes(newStructure.type)) {
      payload.capacity = newStructure.capacity ? Number(newStructure.capacity) : null;
    }

    try {
      const res = await api.post(
        `/farms/workspace/${newStructure.type}s`,
        payload,
        { headers: { "X-Farm-ID": farmId } }
      );

      setStructures((prev) => ({
        ...prev,
        [`${newStructure.type}s`]: [...prev[`${newStructure.type}s`], res.data],
      }));

      setNewStructure({ type: "", name: "", area: "", capacity: "" });
    } catch (err) {
      console.error("Error adding structure:", err);
      alert("Error adding structure");
    }
  };

  // ------------------------------------------------
  // UI
  // ------------------------------------------------
  return (
    <div className="dashboard-container">
      <h1>{farm.name}</h1>

      <p>
        <strong>Location:</strong> {farm.location}
        <br />
        <strong>Size:</strong> {farm.size}
      </p>

      <hr />

      <h2>Add Structure</h2>

      <select
        value={newStructure.type}
        onChange={(e) => setNewStructure({ ...newStructure, type: e.target.value })}
      >
        <option value="">Select Type</option>
        {availableTypes.map((t) => (
          <option key={t} value={t}>{t}</option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Structure Name"
        value={newStructure.name}
        onChange={(e) => setNewStructure({ ...newStructure, name: e.target.value })}
      />

      {["block", "greenhouse", "pond"].includes(newStructure.type) && (
        <input
          type="number"
          placeholder="Area"
          value={newStructure.area}
          onChange={(e) => setNewStructure({ ...newStructure, area: e.target.value })}
        />
      )}

      {["barn", "coop"].includes(newStructure.type) && (
        <input
          type="number"
          placeholder="Capacity"
          value={newStructure.capacity}
          onChange={(e) => setNewStructure({ ...newStructure, capacity: e.target.value })}
        />
      )}

      <button onClick={handleAddStructure}>Add Structure</button>

      <hr />

      <UnitToggle unit={unit} setUnit={setUnit} />

      <h2>Blocks</h2>
      <div className="grid">
        {structures.blocks.length
          ? structures.blocks.map((s) => <StructureCard key={s.id} structure={s} type="block" unit={unit} />)
          : <p>No blocks yet</p>}
      </div>

      <h2>Greenhouses</h2>
      <div className="grid">
        {structures.greenhouses.length
          ? structures.greenhouses.map((s) => <StructureCard key={s.id} structure={s} type="greenhouse" unit={unit} />)
          : <p>No greenhouses yet</p>}
      </div>

      <h2>Barns</h2>
      <div className="grid">
        {structures.barns.length
          ? structures.barns.map((s) => <StructureCard key={s.id} structure={s} type="barn" unit={unit} />)
          : <p>No barns yet</p>}
      </div>

      <h2>Coops</h2>
      <div className="grid">
        {structures.coops.length
          ? structures.coops.map((s) => <StructureCard key={s.id} structure={s} type="coop" unit={unit} />)
          : <p>No coops yet</p>}
      </div>

      <h2>Ponds</h2>
      <div className="grid">
        {structures.ponds.length
          ? structures.ponds.map((s) => <StructureCard key={s.id} structure={s} type="pond" unit={unit} />)
          : <p>No ponds yet</p>}
      </div>
    </div>
  );
}
