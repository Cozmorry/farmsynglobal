
// src/components/hr/pages/HRPayementList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { getHRPayments, getCasualWorkers, getPermanentStaff } from "../api/hrApi";
import { useNavigate } from "react-router-dom";

export default function HRPaymentList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [casualWorkers, setCasualWorkers] = useState([]);
  const [permanentStaff, setPermanentStaff] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch HR payments
        const paymentsRes = await getHRPayments();
        const payments = paymentsRes.data || [];

        // Fetch workers
        const casualRes = await getCasualWorkers(1); // farm_id = 1
        const permanentRes = await getPermanentStaff(1);

        setCasualWorkers(casualRes.data || []);
        setPermanentStaff(permanentRes.data || []);

        // Map worker IDs to names
        const mappedRows = payments.map((p) => {
          let workerName = p.staff_id;
          if (p.worker_type === "casual") {
            const worker = casualRes.data.find((w) => w.id === p.staff_id);
            workerName = worker ? worker.name : p.staff_id;
          } else if (p.worker_type === "permanent") {
            const staff = permanentRes.data.find((s) => s.id === p.staff_id);
            workerName = staff ? staff.name : p.staff_id;
          }
          return { ...p, worker_name: workerName };
        });

        setRows(mappedRows);
      } catch (err) {
        console.error("Error fetching payments or workers:", err);
      }
    };

    fetchData();
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "worker_type", headerName: "Type", width: 120 },
    { field: "worker_name", headerName: "Worker", width: 200 }, // display name
    { field: "amount", headerName: "Amount", width: 130 },
    { field: "payment_method", headerName: "Method", width: 150 },
    {
      field: "payment_date",
      headerName: "Date",
      width: 160,
      valueGetter: (params) =>
        params.row.payment_date
          ? new Date(params.row.payment_date).toLocaleDateString()
          : "",
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        HR Payments
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/hr/payments/new")}
      >
        Record Payment
      </Button>

      <Paper sx={{ height: 600 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}
