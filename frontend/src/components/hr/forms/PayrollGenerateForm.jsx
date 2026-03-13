// src/components/hr/forms/PayrollGenerateForm.jsx
import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Grid,
  Paper,
  TextField,
  Typography,
  MenuItem,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { generatePayroll, getPermanentStaff, getCasualWorkers } from "../api/hrApi";

export default function PayrollGenerateForm() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    worker_type: "permanent",
    employee_id: "",
    period_start: "",
    period_end: "",
  });

  const [permanentStaff, setPermanentStaff] = useState([]);
  const [casualWorkers, setCasualWorkers] = useState([]);

  useEffect(() => {
    getPermanentStaff(1).then((res) => setPermanentStaff(res.data));
    getCasualWorkers(1).then((res) => setCasualWorkers(res.data));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await generatePayroll(form.employee_id, form.period_start, form.period_end);
    navigate("/hr/payroll");
  };

  const employeeList =
    form.worker_type === "permanent" ? permanentStaff : casualWorkers;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Generate Payroll
      </Typography>

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>

            {/* Worker Type */}
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Worker Type"
                value={form.worker_type}
                onChange={(e) =>
                  setForm({ ...form, worker_type: e.target.value, employee_id: "" })
                }
              >
                <MenuItem value="permanent">Permanent Staff</MenuItem>
                <MenuItem value="casual">Casual Worker</MenuItem>
              </TextField>
            </Grid>

            {/* Employee Selection */}
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Employee"
                value={form.employee_id}
                onChange={(e) =>
                  setForm({ ...form, employee_id: e.target.value })
                }
                required
              >
                {employeeList.map((worker) => (
                  <MenuItem key={worker.id} value={worker.id}>
                    {worker.name}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* Period Start */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                type="date"
                label="Period Start"
                InputLabelProps={{ shrink: true }}
                value={form.period_start}
                onChange={(e) =>
                  setForm({ ...form, period_start: e.target.value })
                }
                required
              />
            </Grid>

            {/* Period End */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                type="date"
                label="Period End"
                InputLabelProps={{ shrink: true }}
                value={form.period_end}
                onChange={(e) =>
                  setForm({ ...form, period_end: e.target.value })
                }
                required
              />
            </Grid>

            {/* Submit */}
            <Grid item xs={12}>
              <Button variant="contained" type="submit">
                Generate Payroll
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}
