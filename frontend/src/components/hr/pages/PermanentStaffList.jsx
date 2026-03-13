
// src/components/hr/pages/PermanentStaffList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getPermanentStaff, deactivatePermanentStaff } from "../api/hrApi";

export default function PermanentStaffList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const farm_id = 1; // can be dynamic later

  const loadStaff = async () => {
    setLoading(true);
    try {
      const res = await getPermanentStaff(farm_id);
      setRows(res.data || []);
    } catch (err) {
      console.error("Error loading permanent staff:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStaff();
  }, []);

  const handleDeactivate = async (id) => {
    if (window.confirm("Are you sure you want to deactivate this staff?")) {
      try {
        await deactivatePermanentStaff(id);
        loadStaff();
      } catch (err) {
        console.error("Error deactivating staff:", err);
      }
    }
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "name", headerName: "Name", width: 200 },
    { field: "position", headerName: "Position", width: 150 },
    { field: "salary", headerName: "Salary", width: 130 },
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
            onClick={() => navigate(`/hr/permanent/edit/${params.row.id}`)}
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
        Permanent Staff
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/hr/permanent/new")}
      >
        Add Permanent Staff
      </Button>

      <Paper sx={{ height: 600 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} loading={loading} />
      </Paper>
    </Box>
  );
}
