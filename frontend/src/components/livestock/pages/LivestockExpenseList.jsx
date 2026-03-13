// src/components/livestock/pages/LivestockExpenseList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import LivestockSubmoduleCreate from "../forms/LivestockSubmoduleForm";

export default function LivestockExpenseList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    getExpenses().then((res) => setRows(res.data));
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "livestock_id", headerName: "Animal ID", width: 100 },
    { field: "category", headerName: "Category", width: 150 },
    { field: "sub_category", headerName: "Sub Category", width: 150 },
    { field: "amount", headerName: "Amount", width: 100 },
    { field: "date", headerName: "Date", width: 120 },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button variant="outlined" size="small" onClick={() => navigate(`/livestock/expenses/edit/${params.row.id}`)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Livestock Expenses
      </Typography>

      <Button variant="contained" sx={{ mb: 2 }} onClick={() => navigate("/livestock/expenses/new")}>
        Add Expense
      </Button>

      <Paper elevation={2} sx={{ height: 600, p: 2 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}


