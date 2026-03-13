// src/components/livestock/pages/LivestockFeedingList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import LivestockSubmoduleCreate from "../forms/LivestockSubmoduleForm";

export default function LivestockFeedingList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getFeedings().then((res) => setRows(res.data));
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "livestock_id", headerName: "Animal ID", width: 100 },
    { field: "group_id", headerName: "Group ID", width: 100 },
    { field: "feed_item_id", headerName: "Feed Item", width: 120 },
    { field: "quantity", headerName: "Qty", width: 80 },
    { field: "feeding_method", headerName: "Method", width: 120 },
    { field: "feeding_date", headerName: "Date", width: 120 },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button variant="outlined" size="small" onClick={() => navigate(`/livestock/feeding/edit/${params.row.id}`)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Livestock Feeding
      </Typography>

      <Button variant="contained" sx={{ mb: 2 }} onClick={() => navigate("/livestock/feeding/new")}>
        Add Feeding
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}

