// src/components/UnitToggle.jsx
import React from "react";

export default function UnitToggle({ unit, setUnit }) {
  return (
    <div style={{ marginBottom: "15px" }}>
      <label style={{ marginRight: "10px" }}>Unit:</label>
      <button
        onClick={() => setUnit("ha")}
        style={{
          marginRight: "5px",
          padding: "5px 10px",
          backgroundColor: unit === "ha" ? "#4caf50" : "#ccc",
          color: unit === "ha" ? "#fff" : "#000",
          border: "none",
          borderRadius: "3px",
          cursor: "pointer",
        }}
      >
        Hectares
      </button>
      <button
        onClick={() => setUnit("acre")}
        style={{
          padding: "5px 10px",
          backgroundColor: unit === "acre" ? "#4caf50" : "#ccc",
          color: unit === "acre" ? "#fff" : "#000",
          border: "none",
          borderRadius: "3px",
          cursor: "pointer",
        }}
      >
        Acres
      </button>
    </div>
  );
}
