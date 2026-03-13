//src/components/ Farms/FarmWizard.jsx
import React, { useState, useContext } from "react";
import api from "../../api/axios";
import { UsersContext } from "../../context/UsersContext";
import { TenantContext } from "../../context/TenantContext";

export default function FarmWizard() {
  const { currentTenant } = useContext(TenantContext);
  const { user, refreshFarms } = useContext(UsersContext);

  const [step, setStep] = useState(1);
  const [farm, setFarm] = useState({
    name: "",
    location: "",
    farm_type: "crop",
    scale: "small",
    size: { value: 1, unit: "ha" },
    active_modules: [],
  });

  const FARM_TYPES = ["crop", "livestock", "poultry", "aquaculture", "mixed"];
  const SCALES = ["small", "medium", "large"];

  const handleNext = async () => {
    if (step === 1) {
      // Create farm
      const res = await api.post("/farms", farm);
      setFarm(res.data);
      // Refresh user's farms in context
      refreshFarms();
      setStep(2);
    } else if (step === 2) {
      setStep(3);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px" }}>
      <h2>Farm Onboarding</h2>

      {step === 1 && (
        <div>
          <input
            placeholder="Farm Name"
            value={farm.name}
            onChange={(e) => setFarm({ ...farm, name: e.target.value })}
          />
          <input
            placeholder="Location"
            value={farm.location}
            onChange={(e) => setFarm({ ...farm, location: e.target.value })}
          />
          <select value={farm.farm_type} onChange={(e) => setFarm({ ...farm, farm_type: e.target.value })}>
            {FARM_TYPES.map((type) => <option key={type} value={type}>{type.toUpperCase()}</option>)}
          </select>
          <select value={farm.scale} onChange={(e) => setFarm({ ...farm, scale: e.target.value })}>
            {SCALES.map((scale) => <option key={scale} value={scale}>{scale.toUpperCase()}</option>)}
          </select>
          <input
            type="number"
            placeholder="Size"
            value={farm.size.value}
            onChange={(e) => setFarm({ ...farm, size: { ...farm.size, value: parseFloat(e.target.value) } })}
          />
          <select value={farm.size.unit} onChange={(e) => setFarm({ ...farm, size: { ...farm.size, unit: e.target.value } })}>
            <option value="ha">HA</option>
            <option value="ac">AC</option>
          </select>
        </div>
      )}

      {step === 2 && (
        <div>
          <h3>Success!</h3>
          <p>Farm <strong>{farm.name}</strong> created with default structures:</p>
          <ul>
            {farm.barns?.map((b) => <li key={b.id}>{b.name}</li>)}
            {farm.coops?.map((c) => <li key={c.id}>{c.name}</li>)}
            {farm.ponds?.map((p) => <li key={p.id}>{p.name}</li>)}
          </ul>
        </div>
      )}

      {step < 3 && <button onClick={handleNext}>Next</button>}
    </div>
  );
}
