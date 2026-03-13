// src/components/farms/StructureCard.jsx
import React from "react";

// Conversion helper: 1 hectare = 2.47105 acres
const convertArea = (areaHa, unit) => {
  if (areaHa == null) return "N/A";
  if (unit === "ha") return `${areaHa} ha`;
  if (unit === "acre") return `${(areaHa * 2.47105).toFixed(2)} acres`;
  return areaHa;
};

export default function StructureCard({ structure, type, unit }) {
  const displayValue =
    ["block", "greenhouse", "pond"].includes(type)
      ? `Area: ${convertArea(structure.area, unit)}`
      : `Capacity: ${structure.capacity ?? "N/A"}`;

  return (
    <div className="dashboard-card">
      <h3>{structure.name}</h3>
      <p>{displayValue}</p>
    </div>
  );
}
