// src/components/livestock/LivestockDashboard.jsx

import React, { useEffect, useState } from "react";
import { Box, Grid, Paper, Typography, Button } from "@mui/material";
import { Link, useParams } from "react-router-dom";

import {
  livestock,
  groups,
  productions,
  sales,
} from "../api/LivestockApi";

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

export default function LivestockDashboard() {
  const { barnId } = useParams();

  const [stats, setStats] = useState({
    livestock: 0,
    groups: 0,
    productions: 0,
    sales: 0,
  });

  useEffect(() => {
    const loadStats = async () => {
      try {
        const filters = {};
        if (barnId) filters.barn_id = barnId;

        const [
          livestockRes,
          groupsRes,
          productionsRes,
          salesRes,
        ] = await Promise.all([
          livestock.list(filters),
          groups.list(filters),
          productions.list(filters),
          sales.list(filters),
        ]);

        setStats({
          livestock: livestockRes.data?.length || 0,
          groups: groupsRes.data?.length || 0,
          productions: productionsRes.data?.length || 0,
          sales: salesRes.data?.length || 0,
        });
      } catch (error) {
        console.error("Livestock dashboard load error:", error);
      }
    };

    loadStats();
  }, [barnId]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Livestock Management Dashboard
        {barnId && ` — Barn ${barnId}`}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <StatCard title="Total Livestock" value={stats.livestock} link="/livestock/animals/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Groups / Herds" value={stats.groups} link="/livestock/groups/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Production Records" value={stats.productions} link="/livestock/productions/new" />
        </Grid>

        <Grid item xs={12} md={3}>
          <StatCard title="Sales Records" value={stats.sales} link="/livestock/sales/new" />
        </Grid>
      </Grid>
    </Box>
  );
}
