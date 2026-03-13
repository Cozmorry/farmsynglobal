// src/components/hr/forms/HRPayementForm.jsx
import React, { useEffect, useState } from "react";
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
import { createHRPayment, getCasualWorkers, getPermanentStaff } from "../api/hrApi";

export default function HRPaymentForm() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    farm_id: 1,
    worker_type: "casual",
    staff_id: "",
    amount: 0,
    payment_method: "cash",
    description: "",
    payment_date: new Date().toISOString().slice(0, 10),
  });

  const [workers, setWorkers] = useState([]);

  // Load workers based on selected type
  useEffect(() => {
    const fetchWorkers = async () => {
      try {
        if (form.worker_type === "casual") {
          const res = await getCasualWorkers(form.farm_id);
          setWorkers(res.data || []);
        } else if (form.worker_type === "permanent") {
          const res = await getPermanentStaff(form.farm_id);
          setWorkers(res.data || []);
        }
        setForm((prev) => ({ ...prev, staff_id: "" })); // reset selection
      } catch (err) {
        console.error("Error fetching workers:", err);
      }
    };

    fetchWorkers();
  }, [form.worker_type, form.farm_id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createHRPayment(form);
    navigate("/hr/payments");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Record HR Payment
      </Typography>

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Worker Type"
                value={form.worker_type}
                onChange={(e) =>
                  setForm({ ...form, worker_type: e.target.value })
                }
              >
                <MenuItem value="casual">Casual</MenuItem>
                <MenuItem value="permanent">Permanent</MenuItem>
              </TextField>
            </Grid>

            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Select Worker"
                value={form.staff_id}
                onChange={(e) =>
                  setForm({ ...form, staff_id: e.target.value })
                }
                required
              >
                {workers.map((worker) => (
                  <MenuItem key={worker.id} value={worker.id}>
                    {worker.name} ({worker.id})
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                type="number"
                label="Amount"
                value={form.amount}
                onChange={(e) =>
                  setForm({ ...form, amount: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Payment Method"
                value={form.payment_method}
                onChange={(e) =>
                  setForm({ ...form, payment_method: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                type="date"
                label="Payment Date"
                InputLabelProps={{ shrink: true }}
                value={form.payment_date}
                onChange={(e) =>
                  setForm({ ...form, payment_date: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={12}>
              <Button variant="contained" type="submit">
                Save Payment
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}

