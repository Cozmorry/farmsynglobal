//src/components/poultry/pages/PoultrySaleList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getSales } from "../api/poultryApi";

export default function PoultrySaleList({ batchId }) {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getSales(batchId ? { batch_id: batchId } : {})
      .then((res) => setRows(res.data));
  }, [batchId]);


  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "product_type", headerName: "Product", width: 150 },
    { field: "batch_id", headerName: "Batch ID", width: 100 },
    { field: "quantity", headerName: "Qty", width: 100 },
    { field: "price", headerName: "Price", width: 100 },
    { field: "date", headerName: "Date", width: 150, valueGetter: (params) => params.row.date ? new Date(params.row.date).toLocaleDateString() : "" },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button variant="outlined" size="small" onClick={() => navigate(`/poultry/sales/edit/${params.row.id}`)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Poultry Sales
      </Typography>

      <Button variant="contained" sx={{ mb: 2 }} onClick={() => navigate("/poultry/sales/new")}>
        Add Sale
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}
