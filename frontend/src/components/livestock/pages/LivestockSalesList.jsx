// src/components/livestock/pages/LivestockSalesList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import LivestockSubmoduleCreate from "../forms/LivestockSubmoduleForm";

export default function LivestockSalesList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getSales().then((res) => setRows(res.data));
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "livestock_id", headerName: "Animal ID", width: 100 },
    { field: "production_type", headerName: "Type", width: 120 },
    { field: "quantity", headerName: "Quantity", width: 100 },
    { field: "unit_price", headerName: "Unit Price", width: 100 },
    { field: "total_sale", headerName: "Total Sale", width: 120 },
    { field: "buyer_name", headerName: "Buyer", width: 150 },
    { field: "date", headerName: "Date", width: 120 },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button variant="outlined" size="small" onClick={() => navigate(`/livestock/sales/edit/${params.row.id}`)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Livestock Sales
      </Typography>

      <Button variant="contained" sx={{ mb: 2 }} onClick={() => navigate("/livestock/sales/new")}>
        Add Sale
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}

