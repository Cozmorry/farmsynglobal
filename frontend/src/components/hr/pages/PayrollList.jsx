// src/components/hr/pages/PayrollList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { getPayrolls, getPermanentStaff, getCasualWorkers } from "../api/hrApi";

export default function PayrollList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [permanentStaff, setPermanentStaff] = useState([]);
  const [casualWorkers, setCasualWorkers] = useState([]);

  useEffect(() => {
    // Fetch payrolls
    getPayrolls().then((res) => setRows(res.data));

    // Fetch staff lists
    getPermanentStaff(1).then((res) => setPermanentStaff(res.data));
    getCasualWorkers(1).then((res) => setCasualWorkers(res.data));
  }, []);

  // Helper to get employee name
  const getEmployeeName = (id) => {
    const perm = permanentStaff.find((p) => p.id === id);
    if (perm) return perm.name;
    const casual = casualWorkers.find((c) => c.id === id);
    if (casual) return casual.name;
    return "Unknown";
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    {
      field: "employee_name",
      headerName: "Employee Name",
      width: 200,
      valueGetter: (params) => getEmployeeName(params.row.employee_id),
    },
    {
      field: "employee_id",
      headerName: "Employee ID",
      width: 130,
    },
    {
      field: "period_start",
      headerName: "From",
      width: 130,
    },
    {
      field: "period_end",
      headerName: "To",
      width: 130,
    },
    {
      field: "gross_pay",
      headerName: "Gross",
      width: 120,
    },
    {
      field: "deductions",
      headerName: "Deductions",
      width: 130,
    },
    {
      field: "net_pay",
      headerName: "Net Pay",
      width: 120,
    },
    {
      field: "paid_on",
      headerName: "Paid On",
      width: 140,
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Payroll
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/hr/payroll/generate")}
      >
        Generate Payroll
      </Button>

      <Paper sx={{ height: 600 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}

