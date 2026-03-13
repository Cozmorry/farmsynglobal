// src/components/DashboardCard.jsx
// src/components/DashboardCard.jsx
export default function DashboardCard({ title, value }) {
  return (
    <div style={{
      backgroundColor: "#fff",
      padding: 20,
      borderRadius: 8,
      boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
      minWidth: 200,
      flex: "1 1 200px",
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center"
    }}>
      <h3 style={{ margin: 0, fontSize: 18, color: "#34495e" }}>{title}</h3>
      <p style={{ fontSize: 24, fontWeight: "bold", margin: "10px 0 0" }}>{value}</p>
    </div>
  );
}

