// src/components/poultry/forms/PoultryProductionForm.jsx
import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Grid,
  Paper,
  TextField,
  Typography,
  MenuItem,
} from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import {
  getProduction,
  createProduction,
  updateProduction,
  getBatches,
} from "../api/poultryApi";
import { normalizeDate, number } from "./utils";

export default function PoultryProductionForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [batches, setBatches] = useState([]);

  const [form, setForm] = useState({
    batch_id: "",
    production_type: "EGGS",
    quantity: "",
    date: "",
  });

  /* Load batches */
  useEffect(() => {
    getBatches().then((res) => setBatches(res.data || []));
  }, []);

  /* Load record if editing */
  useEffect(() => {
    if (!id) return;

    getProduction(id).then((res) =>
      setForm({
        ...res.data,
        batch_id: number(res.data.batch_id),
        quantity: number(res.data.quantity),
        date: normalizeDate(res.data.date),
      })
    );
  }, [id]);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      ...form,
      batch_id: number(form.batch_id),
      quantity: number(form.quantity),
    };

    if (id) await updateProduction(id, payload);
    else await createProduction(payload);

    navigate("/poultry/productions");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} mb={3}>
        {id ? "Edit Production" : "New Production"}
      </Typography>

      <Paper sx={{ p: 3 }}>
        <form onSubmit={submit}>
          <Grid container spacing={2}>
            {/* Batch */}
            <Grid item xs={6}>
              <TextField
                select
                fullWidth
                label="Batch"
                value={form.batch_id}
                onChange={(e) =>
                  setForm({ ...form, batch_id: e.target.value })
                }
                required
              >
                {batches.map((batch) => (
                  <MenuItem key={batch.id} value={batch.id}>
                    {batch.name}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* Production Type */}
            <Grid item xs={6}>
              <TextField
                select
                fullWidth
                label="Production Type"
                value={form.production_type}
                onChange={(e) =>
                  setForm({ ...form, production_type: e.target.value })
                }
              >
                {["EGGS", "CHICKEN"].map((t) => (
                  <MenuItem key={t} value={t}>
                    {t}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* Quantity */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Quantity"
                type="number"
                value={form.quantity}
                onChange={(e) =>
                  setForm({ ...form, quantity: e.target.value })
                }
                required
              />
            </Grid>

            {/* Date */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Date"
                type="date"
                value={form.date}
                InputLabelProps={{ shrink: true }}
                onChange={(e) =>
                  setForm({ ...form, date: e.target.value })
                }
                required
              />
            </Grid>

            <Grid item xs={12}>
              <Button type="submit" variant="contained" disabled={loading}>
                {id ? "Update Production" : "Create Production"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}
