// src/components/hr/pages/CasualWorkerList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getCasualWorkers, deactivateCasualWorker } from "../api/hrApi";

export default function CasualWorkerList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);

  const farm_id = 1; // hardcoded for now, can be dynamic later

  const loadWorkers = async () => {
    setLoading(true);
    try {
      const res = await getCasualWorkers(farm_id);
      setRows(res.data || []);
    } catch (err) {
      console.error("Error loading casual workers:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorkers();
  }, []);

  const handleDeactivate = async (id) => {
    if (window.confirm("Are you sure you want to deactivate this worker?")) {
      try {
        await deactivateCasualWorker(id);
        loadWorkers(); // refresh list
      } catch (err) {
        console.error("Error deactivating worker:", err);
      }
    }
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "name", headerName: "Name", width: 200 },
    { field: "skill", headerName: "Skill", width: 150 },
    { field: "daily_rate", headerName: "Daily Rate", width: 130 },
    { field: "total_days_worked", headerName: "Days", width: 100 },
    { field: "total_pay", headerName: "Total Pay", width: 130 },
    { field: "status", headerName: "Status", width: 120 },
    {
      field: "actions",
      headerName: "Actions",
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: "flex", gap: 1 }}>
          <Button
            size="small"
            variant="outlined"
            onClick={() => navigate(`/hr/casual/edit/${params.row.id}`)}
          >
            Edit
          </Button>
          <Button
            size="small"
            variant="contained"
            color="error"
            onClick={() => handleDeactivate(params.row.id)}
          >
            Deactivate
          </Button>
        </Box>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Casual Workers
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/hr/casual/new")}
      >
        Add Casual Worker
      </Button>

      <Paper sx={{ height: 600 }}>
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={10}
          loading={loading}
        />
      </Paper>
    </Box>
  );
}

