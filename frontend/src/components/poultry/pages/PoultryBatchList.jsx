// src/components/poultry/pages/PoultryBatchList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getBatches } from "../api/poultryApi";

export default function PoultryBatchList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getBatches().then((res) => setRows(res.data));
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "name", headerName: "Batch Name", width: 150 },
    { field: "start_date", headerName: "Start Date", width: 150 },
    { field: "end_date", headerName: "End Date", width: 150 },
    { field: "actions", headerName: "Actions", width: 150, renderCell: (params) => (
      <Button variant="outlined" size="small" onClick={() => navigate(`/poultry/batches/edit/${params.row.id}`)}>
        Edit
      </Button>
    )},
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Poultry Batches
      </Typography>

      <Button variant="contained" sx={{ mb: 2 }} onClick={() => navigate("/poultry/batches/new")}>
        Add Batch
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}
