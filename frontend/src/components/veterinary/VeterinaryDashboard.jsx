// src/components/veterinary/VeterinaryDashboard.jsx
import React, { useEffect, useState } from "react";
import { Box, Grid, Paper, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";

import {
  getVeterinaryRecommendations,
  getVeterinaryRecommendationUploads,
} from "./api/veterinaryApi";

import { getVeterinaryHealthRecords } from "./api/veterinaryHealthApi";

// Stat card component
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
          View
        </Button>
      </Box>
    )}
  </Paper>
);

export default function VeterinaryDashboard({ animalGroupId = 1, groupType = "livestock" }) {
  const [stats, setStats] = useState({
    health: 0,
    recommendations: 0,
    uploads: 0,
  });

  const [reminders, setReminders] = useState([]);

  // Load stats
  useEffect(() => {
    const loadStats = async () => {
      try {
        const [healthRes, recRes, uploadRes] = await Promise.all([
          getVeterinaryHealthRecords(animalGroupId, groupType),
          getVeterinaryRecommendations(),
          getVeterinaryRecommendationUploads({ recommendation_id: animalGroupId }),
        ]);

        const healthCount = healthRes?.length || 0;
        const recCount = recRes?.length || 0;
        const uploadCount = uploadRes?.length || 0;

        setStats({
          health: healthCount,
          recommendations: recCount,
          uploads: uploadCount,
        });

        // Auto-generate reminders
        const newReminders = [];
        if (healthCount === 0) newReminders.push("No health records found for this group.");
        if (recCount === 0) newReminders.push("No veterinary recommendations available.");
        if (uploadCount === 0) newReminders.push("No files uploaded yet.");
        setReminders(newReminders);
      } catch (err) {
        console.error("Veterinary dashboard error:", err);
      }
    };

    loadStats();
  }, [animalGroupId, groupType]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Veterinary Dashboard
      </Typography>

      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} md={4}>
          <StatCard
            title="Health Records"
            value={stats.health}
            link="/veterinary/health"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <StatCard
            title="Recommendations"
            value={stats.recommendations}
            link="/veterinary/recommendations"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <StatCard
            title="Uploaded Files"
            value={stats.uploads}
            link="/veterinary/recommendations"
          />
        </Grid>
      </Grid>

      {reminders.length > 0 && (
        <Box>
          <Typography variant="h6" mb={1}>
            Reminders
          </Typography>
          <ul>
            {reminders.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </Box>
      )}
    </Box>
  );
}
