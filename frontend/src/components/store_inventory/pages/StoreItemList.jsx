// src/components/store_inventory/pages/StoreItemList.jsx

import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getStoreItems } from "../api/storeInventoryApi";

export default function StoreItemList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getStoreItems().then((res) => setRows(res.data));
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 80 },
    { field: "name", headerName: "Item Name", width: 180 },
    { field: "category", headerName: "Category", width: 140 },
    { field: "module_type", headerName: "Module", width: 130 },
    { field: "quantity_in_stock", headerName: "Stock", width: 120 },
    { field: "unit_cost", headerName: "Unit Cost", width: 120 },
    { field: "total_value", headerName: "Total Value", width: 140 },

    {
      field: "actions",
      headerName: "Actions",
      sortable: false,
      width: 180,
      renderCell: (params) => (
        <Button
          variant="outlined"
          size="small"
          onClick={() => navigate(`/store-inventory/items/edit/${params.row.id}`)}
        >
          Edit
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Store Items
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/store-inventory/items/new")}
      >
        Add New Item
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}
