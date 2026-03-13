// src/components/livestock/pages/LivestockBreedingList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { breeding } from "../api/livestockApi";

export default function LivestockBreedingList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    LivestockApi.breeding.list().then((res) => setRows(res.data));
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "dam_id", headerName: "Dam ID", width: 120 },
    { field: "sire_id", headerName: "Sire ID", width: 120 },
    { field: "service_date", headerName: "Service Date", width: 140 },
    { field: "expected_birth_date", headerName: "Expected Birth", width: 160 },
    { field: "actual_birth_date", headerName: "Actual Birth", width: 160 },
    { field: "offspring_count", headerName: "Offspring", width: 120 },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button
          variant="outlined"
          size="small"
          onClick={() =>
            navigate(`/livestock/breeding/edit/${params.row.id}`)
          }
        >
          Edit
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Livestock Breeding Records
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/livestock/breeding/new")}
      >
        Add Breeding Record
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}
