// src/components/hr/forms/WorkSessionForm.jsx
import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Grid,
  MenuItem,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { createWorkSession, getPermanentStaff, getCasualWorkers } from "../api/hrApi";

export default function WorkSessionForm() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    farm_id: 1,
    worker_type: "casual",
    staff_id: "",
    activity: "",
    hours_worked: 0,
    wage_rate: 0,
    total_amount: 0,
    date: new Date().toISOString().slice(0, 10),
  });

  const [permanentStaff, setPermanentStaff] = useState([]);
  const [casualWorkers, setCasualWorkers] = useState([]);

  // Fetch staff lists
  useEffect(() => {
    getPermanentStaff(1).then((res) => setPermanentStaff(res.data));
    getCasualWorkers(1).then((res) => setCasualWorkers(res.data));
  }, []);

  // Get options based on worker_type
  const getWorkerOptions = () =>
    form.worker_type === "casual" ? casualWorkers : permanentStaff;

  // Auto-calc total amount
  const handleChange = (field, value) => {
    const updated = { ...form, [field]: value };
    updated.total_amount =
      Number(updated.hours_worked) * Number(updated.wage_rate);
    setForm(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createWorkSession(form);
    navigate("/hr/work-sessions");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        New Work Session
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
                onChange={(e) => handleChange("worker_type", e.target.value)}
              >
                <MenuItem value="casual">Casual</MenuItem>
                <MenuItem value="permanent">Permanent</MenuItem>
              </TextField>
            </Grid>

            {/* Worker ID (Dropdown) */}
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Worker"
                value={form.staff_id}
                onChange={(e) => handleChange("staff_id", e.target.value)}
                required
              >
                {getWorkerOptions().map((worker) => (
                  <MenuItem key={worker.id} value={worker.id}>
                    {worker.name} (ID: {worker.id})
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* Activity */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Activity"
                value={form.activity}
                onChange={(e) => handleChange("activity", e.target.value)}
                required
              />
            </Grid>

            {/* Hours */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                type="number"
                label="Hours Worked"
                value={form.hours_worked}
                onChange={(e) => handleChange("hours_worked", e.target.value)}
              />
            </Grid>

            {/* Rate */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                type="number"
                label="Wage Rate"
                value={form.wage_rate}
                onChange={(e) => handleChange("wage_rate", e.target.value)}
              />
            </Grid>

            {/* Total */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Total Amount"
                value={form.total_amount}
                InputProps={{ readOnly: true }}
              />
            </Grid>

            {/* Date */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                type="date"
                label="Date"
                InputLabelProps={{ shrink: true }}
                value={form.date}
                onChange={(e) => handleChange("date", e.target.value)}
              />
            </Grid>

            <Grid item xs={12}>
              <Button variant="contained" type="submit">
                Save Work Session
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}
