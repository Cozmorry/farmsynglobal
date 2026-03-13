// src/components/aquaculture/pages/AquacultureDashboard.jsx

import React, { useEffect, useState } from "react";
import { Box, Grid, Paper, Typography, Button } from "@mui/material";
import { Link, useParams } from "react-router-dom";

import {
  getPonds,
  getWaterRecords,
  getProductions,
  getHealth,
} from "../api/aquacultureApi";

const StatCard = ({ title, value, link }) => (
  <Paper sx={{ p: 3 }}>
    <Typography variant="subtitle2" color="text.secondary">
      {title}
    </Typography>
    <Typography variant="h4" fontWeight={700}>
      {value}
    </Typography>
    {link && (
      <Box sx={{ mt: 2 }}>
        <Button component={Link} to={link} variant="contained" size="small">
          Add New
        </Button>
      </Box>
    )}
  </Paper>
);

export default function AquacultureDashboard() {
  const { pondId } = useParams();

  const [stats, setStats] = useState({
    ponds: 0,
    waterRecords: 0,
    productions: 0,
    health: 0,
  });

  useEffect(() => {
    const loadStats = async () => {
      try {
        const filters = {};
        if (pondId) filters.pond_id = pondId;

        const [
          pondsRes,
          waterRes,
          productionRes,
          healthRes,
        ] = await Promise.all([
          getPonds(),
          getWaterRecords(filters),
          getProductions(filters),
          getHealth(filters),
        ]);

        setStats({
          ponds: pondsRes.data.length || 0,
          waterRecords: waterRes.data.length || 0,
          productions: productionRes.data.length || 0,
          health: healthRes.data.length || 0,
        });
      } catch (error) {
        console.error("Aquaculture dashboard load error:", error);
      }
    };

    loadStats();
  }, [pondId]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Aquaculture Management Dashboard
        {pondId && ` — Pond ${pondId}`}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <StatCard title="Total Ponds" value={stats.ponds} link="/aquaculture/ponds/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Water Quality Records" value={stats.waterRecords} link="/aquaculture/water_quality/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Production Records" value={stats.productions} link="/aquaculture/production/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Health Records" value={stats.health} link="/aquaculture/health/new" />
        </Grid>
      </Grid>
    </Box>
  );
}
