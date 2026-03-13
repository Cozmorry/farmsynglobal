// src/components/ui/KpiCard.jsx
export default function KpiCard({ title, value, color = "#0ea5e9" }) {
  return (
    <div
      style={{
        background: "white",
        padding: "20px",
        borderRadius: "14px",
        boxShadow: "0 10px 25px rgba(0,0,0,0.06)",
        borderLeft: `5px solid ${color}`,
        transition: "0.2s",
        cursor: "default",
      }}
    >
      <p style={{ margin: 0, fontSize: "14px", color: "#64748b" }}>{title}</p>
      <h2 style={{ margin: "8px 0 0 0" }}>{value}</h2>
    </div>
  );
}
