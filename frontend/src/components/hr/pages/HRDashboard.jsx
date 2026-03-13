// src/components/hr/pages/HRDashboard.jsx
import React from "react";
import {
  Box,
  Grid,
  Paper,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const Card = ({ title, subtitle, path }) => {
  const navigate = useNavigate();

  return (
    <Paper
      elevation={2}
      sx={{
        p: 3,
        cursor: "pointer",
        height: "100%",
        "&:hover": { boxShadow: 6 },
      }}
      onClick={() => navigate(path)}
    >
      <Typography variant="h6" fontWeight={700}>
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {subtitle}
      </Typography>
    </Paper>
  );
};

export default function HRDashboard() {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" fontWeight={800} sx={{ mb: 4 }}>
        Human Resources
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card
            title="Permanent Staff"
            subtitle="Manage full-time employees"
            path="/hr/permanent"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            title="Casual Workers"
            subtitle="Manage daily workers"
            path="/hr/casual"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            title="Work Sessions"
            subtitle="Attendance & daily work records"
            path="/hr/work-sessions"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            title="Payroll"
            subtitle="Generate and review payroll"
            path="/hr/payroll"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            title="HR Payments"
            subtitle="Record staff payments"
            path="/hr/payments"
          />
        </Grid>
      </Grid>
    </Box>
  );
}
