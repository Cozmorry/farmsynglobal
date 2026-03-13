// src/components/crop-management/pages/CropDashboard.jsx

// src/components/crop-management/pages/CropDashboard.jsx

import React, { useEffect, useState } from "react";
import { Box, Paper, Typography, Button, CircularProgress } from "@mui/material";
import { Link, useParams } from "react-router-dom";
import ModuleTable from "../components/ModuleTable";
import {
  getCrops,
  getSales,
  generalActivities,
  landPreparations,
  nurseryActivities,
  fertilizerApplications,
  chemicalApplications,
  weedingActivities,
  scoutingActivities,
  soilTests,
  soilAmendments,
  cropRotations,
} from "../api/cropManagementApi";

/* ✅ Reusable KPI Tile */
const StatCard = ({ title, value, link }) => (
  <Paper sx={{ p: 3, textAlign: "center" }}>
    <Typography variant="subtitle2" color="text.secondary">
      {title}
    </Typography>
    <Typography variant="h4" fontWeight={700} sx={{ my: 1 }}>
      {value}
    </Typography>
    {link && (
      <Button component={Link} to={link} variant="contained" size="small">
        Add New
      </Button>
    )}
  </Paper>
);

export default function CropDashboard() {
  const { blockId, greenhouseId } = useParams();

  const [stats, setStats] = useState({});
  const [tableData, setTableData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAllData = async () => {
      setLoading(true);

      try {
        // 👇 Build filter object dynamically
        const filters = {};
        if (blockId) filters.block_id = blockId;
        if (greenhouseId) filters.greenhouse_id = greenhouseId;

        const [
          cropsRes,
          salesRes,
          activitiesRes,
          landPrepsRes,
          nurseryRes,
          fertilizerRes,
          chemicalRes,
          weedingRes,
          scoutingRes,
          soilTestsRes,
          soilAmendmentsRes,
          cropRotationsRes,
        ] = await Promise.all([
          getCrops(filters),
          getSales(filters),
          generalActivities.list(filters),
          landPreparations.list(filters),
          nurseryActivities.list(filters),
          fertilizerApplications.list(filters),
          chemicalApplications.list(filters),
          weedingActivities.list(filters),
          scoutingActivities.list(filters),
          soilTests.list(filters),
          soilAmendments.list(filters),
          cropRotations.list(filters),
        ]);

        const newStats = {
          Crops: cropsRes.data.length || 0,
          Sales: salesRes.data.length || 0,
          "Crop Activities": activitiesRes.data.length || 0,
          "Land Preparations": landPrepsRes.data.length || 0,
          "Nursery Activities": nurseryRes.data.length || 0,
          "Fertilizer Applications": fertilizerRes.data.length || 0,
          "Chemical Applications": chemicalRes.data.length || 0,
          Weeding: weedingRes.data.length || 0,
          "Scouting Activities": scoutingRes.data.length || 0,
          "Soil Tests": soilTestsRes.data.length || 0,
          "Soil Amendments": soilAmendmentsRes.data.length || 0,
          "Crop Rotations": cropRotationsRes.data.length || 0,
        };

        setStats(newStats);

        const newTableData = {
          Crops: cropsRes.data,
          Sales: salesRes.data,
          "Crop Activities": activitiesRes.data,
          "Land Preparations": landPrepsRes.data,
          "Nursery Activities": nurseryRes.data,
          "Fertilizer Applications": fertilizerRes.data,
          "Chemical Applications": chemicalRes.data,
          Weeding: weedingRes.data,
          "Scouting Activities": scoutingRes.data,
          "Soil Tests": soilTestsRes.data,
          "Soil Amendments": soilAmendmentsRes.data,
          "Crop Rotations": cropRotationsRes.data,
        };

        setTableData(newTableData);
      } catch (error) {
        console.error("Error fetching crop dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAllData();
  }, [blockId, greenhouseId]);

  if (loading) {
    return (
      <Box sx={{ mt: 10, textAlign: "center" }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Crop Management Dashboard
        {blockId && ` — Block ${blockId}`}
        {greenhouseId && ` — Greenhouse ${greenhouseId}`}
      </Typography>

      {/* KPI Tiles */}
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: 16,
          mb: 4,
        }}
      >
        {Object.entries(stats).map(([key, value]) => (
          <StatCard
            key={key}
            title={key}
            value={value}
            link={`/crop_management/${key.toLowerCase().replace(/\s+/g, "_")}/new`}
          />
        ))}
      </Box>

      {/* Modular Tables */}
      {Object.entries(tableData).map(([title, data]) => (
        <ModuleTable key={title} title={title} data={data} />
      ))}
    </Box>
  );
}
