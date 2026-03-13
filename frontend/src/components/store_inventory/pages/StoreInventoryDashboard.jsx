// src/components/store_inventory/pages/StoreInventoryDashboard.jsx

import React from "react";
import { Box, Grid, Paper, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const DashboardCard = ({ title, value }) => (
  <Paper elevation={3} sx={{ p: 3, textAlign: "center" }}>
    <Typography variant="h6" fontWeight={600}>{title}</Typography>
    <Typography variant="h4" sx={{ mt: 1, fontWeight: 700 }}>{value}</Typography>
  </Paper>
);

export default function StoreInventoryDashboard() {
  const navigate = useNavigate();

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Store Inventory Dashboard
      </Typography>

      {/* Action Buttons */}
      <Box sx={{ mb: 3, display: "flex", gap: 2 }}>
        <Button variant="contained" onClick={() => navigate("/store-inventory/items")}>
          View Store Items
        </Button>
        <Button variant="contained" onClick={() => navigate("/store-inventory/items/new")}>
          Add Store Item
        </Button>
        <Button variant="contained" onClick={() => navigate("/store-inventory/transactions")}>
          View Transactions
        </Button>
        <Button variant="contained" onClick={() => navigate("/store-inventory/transactions/new")}>
          Record Transaction
        </Button>
      </Box>

      {/* Cards */}
      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <DashboardCard title="Total Items" value="—" />
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <DashboardCard title="Total Stock Value" value="—" />
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <DashboardCard title="Transactions Recorded" value="—" />
        </Grid>
      </Grid>
    </Box>
  );
}
