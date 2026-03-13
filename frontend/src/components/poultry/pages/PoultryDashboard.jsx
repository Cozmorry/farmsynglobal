// src/components/poultry/pages/PoultryDashboard.jsx

import React, { useEffect, useState } from "react";
import { Box, Grid, Paper, Typography, Button } from "@mui/material";
import { Link, useParams } from "react-router-dom";

import {
  getBatches,
  getActivities,
  getProductions,
  getSales,
} from "../api/poultryApi";

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

export default function PoultryDashboard() {
  const { coopId } = useParams();

  const [stats, setStats] = useState({
    batches: 0,
    eggs: 0,
    activities: 0,
    sales: 0,
  });

  useEffect(() => {
    const loadStats = async () => {
      try {
        const filters = {};
        if (coopId) filters.coop_id = coopId;

        const [
          batchRes,
          activityRes,
          productionRes,
          salesRes,
        ] = await Promise.all([
          getBatches(filters),
          getActivities(filters),
          getProductions(filters),
          getSales(filters),
        ]);

        const totalEggs = productionRes.data.reduce(
          (sum, p) => sum + Number(p.quantity || 0),
          0
        );

        const totalSales = salesRes.data.reduce(
          (sum, s) => sum + Number(s.total_amount || 0),
          0
        );

        setStats({
          batches: batchRes.data.length || 0,
          activities: activityRes.data.length || 0,
          eggs: totalEggs,
          sales: totalSales,
        });
      } catch (error) {
        console.error("Poultry dashboard load error:", error);
      }
    };

    loadStats();
  }, [coopId]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Poultry Management Dashboard
        {coopId && ` — Coop ${coopId}`}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <StatCard title="Total Batches" value={stats.batches} link="/poultry/batches/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Eggs Produced" value={stats.eggs} link="/poultry/productions/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Activities" value={stats.activities} link="/poultry/activities/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Sales Revenue" value={`₦ ${stats.sales}`} link="/poultry/sales/new" />
        </Grid>
      </Grid>
    </Box>
  );
}
