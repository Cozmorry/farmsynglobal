//src/components/Layout/Header.jsx
import React from "react";

export default function Header() {
  const farmName = localStorage.getItem("farm_name") || "";

  return (
    <header>
      <h1>Farm: {farmName}</h1>
    </header>
  );
}
