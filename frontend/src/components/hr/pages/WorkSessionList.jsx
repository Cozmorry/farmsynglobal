// src/components/hr/pages/WorkSessionList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getWorkSessions, getPermanentStaff, getCasualWorkers } from "../api/hrApi";

export default function WorkSessionList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [permanentStaff, setPermanentStaff] = useState([]);
  const [casualWorkers, setCasualWorkers] = useState([]);

  useEffect(() => {
    getWorkSessions().then((res) => setRows(res.data));
    getPermanentStaff(1).then((res) => setPermanentStaff(res.data));
    getCasualWorkers(1).then((res) => setCasualWorkers(res.data));
  }, []);

  // Helper to get employee name by ID
  const getEmployeeName = (id) => {
    const perm = permanentStaff.find((p) => p.id === id);
    if (perm) return perm.name;
    const casual = casualWorkers.find((c) => c.id === id);
    if (casual) return casual.name;
    return "Unknown";
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "worker_type", headerName: "Type", width: 110 },
    {
      field: "employee_name",
      headerName: "Worker Name",
      width: 180,
      valueGetter: (params) => getEmployeeName(params.row.staff_id),
    },
    { field: "staff_id", headerName: "Worker ID", width: 110 },
    { field: "activity", headerName: "Activity", width: 180 },
    { field: "hours_worked", headerName: "Hours", width: 100 },
    { field: "wage_rate", headerName: "Rate", width: 100 },
    { field: "total_amount", headerName: "Total", width: 120 },
    {
      field: "date",
      headerName: "Date",
      width: 160,
      valueGetter: (params) =>
        params.row.date
          ? new Date(params.row.date).toLocaleDateString()
          : "",
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Work Sessions
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/hr/work-sessions/new")}
      >
        Add Work Session
      </Button>

      <Paper sx={{ height: 600 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}
