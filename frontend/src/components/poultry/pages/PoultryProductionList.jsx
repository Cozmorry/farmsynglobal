//src/components/poultry/pages/PoultryProductionList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getProductions } from "../api/poultryApi";

export default function PoultryProductionList({ batchId }) {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getProductions(batchId ? { batch_id: batchId } : {})
      .then((res) => setRows(res.data));
  }, [batchId]);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "batch_id", headerName: "Batch ID", width: 100 },
    { field: "production_type", headerName: "Type", width: 150 },
    { field: "quantity", headerName: "Qty", width: 100 },
    { field: "date", headerName: "Date", width: 150, valueGetter: (params) => params.row.date ? new Date(params.row.date).toLocaleDateString() : "" },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button variant="outlined" size="small" onClick={() => navigate(`/poultry/productions/edit/${params.row.id}`)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Poultry Production
      </Typography>

      <Button variant="contained" sx={{ mb: 2 }} onClick={() => navigate("/poultry/productions/new")}>
        Add Production
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}
