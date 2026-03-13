// src/components/store_inventory/pages/InventoryTransactionList.jsx

import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getInventoryTransactions } from "../api/storeInventoryApi";

export default function InventoryTransactionList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getInventoryTransactions().then((res) => setRows(res.data));
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "transaction_type", headerName: "Type", width: 110 },
    { field: "quantity", headerName: "Qty", width: 100 },
    { field: "unit_cost", headerName: "Unit Cost", width: 120 },
    { field: "total_cost", headerName: "Total Cost", width: 140 },
    {
      field: "date",
      headerName: "Date",
      width: 180,
      valueGetter: (params) =>
        params.row.date ? new Date(params.row.date).toLocaleString() : "",
    },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button
          variant="outlined"
          size="small"
          onClick={() =>
            navigate(`/store-inventory/transactions/edit/${params.row.id}`)
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
        Inventory Transactions
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/store-inventory/transactions/new")}
      >
        Add Transaction
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}
