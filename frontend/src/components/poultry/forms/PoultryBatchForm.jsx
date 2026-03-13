// src/components/poultry/forms/PoultryBatchForm.jsx

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
import { createBatch, getBatch, updateBatch } from "../api/poultryApi";
import { normalizeDate, number } from "./utils";

export default function PoultryBatchForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    batch_name: "",
    breed: "",
    batch_size: "",
    start_date: "",
    housing_type: "",
    purpose: "",
    source: "",
    expected_cycle_days: "",
    notes: "",
    status: "Active",
  });

  useEffect(() => {
    if (!id) return;

    getBatch(id).then((res) =>
      setForm({
        ...res.data,
        batch_size: number(res.data.batch_size),
        expected_cycle_days: number(res.data.expected_cycle_days),
        start_date: normalizeDate(res.data.start_date),
      })
    );
  }, [id]);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      ...form,
      batch_size: number(form.batch_size),
      expected_cycle_days: number(form.expected_cycle_days),
    };

    if (id) await updateBatch(id, payload);
    else await createBatch(payload);

    navigate("/poultry/batches");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} mb={3}>
        {id ? "Edit Batch" : "New Batch"}
      </Typography>

      <Paper sx={{ p: 3 }}>
        <form onSubmit={submit}>
          <Grid container spacing={2}>
            {/* Batch Name */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Batch Name"
                value={form.batch_name}
                onChange={(e) =>
                  setForm({ ...form, batch_name: e.target.value })
                }
                required
              />
            </Grid>

            {/* Breed */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Breed"
                value={form.breed}
                onChange={(e) => setForm({ ...form, breed: e.target.value })}
              />
            </Grid>

            {/* Batch Size */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Batch Size"
                type="number"
                value={form.batch_size}
                onChange={(e) =>
                  setForm({ ...form, batch_size: e.target.value })
                }
              />
            </Grid>

            {/* Start Date */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Start Date"
                type="date"
                InputLabelProps={{ shrink: true }}
                value={form.start_date}
                onChange={(e) =>
                  setForm({ ...form, start_date: e.target.value })
                }
              />
            </Grid>

            {/* Housing Type */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Housing Type"
                value={form.housing_type}
                onChange={(e) =>
                  setForm({ ...form, housing_type: e.target.value })
                }
              />
            </Grid>

            {/* Purpose */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Purpose"
                value={form.purpose}
                onChange={(e) =>
                  setForm({ ...form, purpose: e.target.value })
                }
              />
            </Grid>

            {/* Source */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Source"
                value={form.source}
                onChange={(e) => setForm({ ...form, source: e.target.value })}
              />
            </Grid>

            {/* Expected Cycle Days */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Expected Cycle Days"
                type="number"
                value={form.expected_cycle_days}
                onChange={(e) =>
                  setForm({ ...form, expected_cycle_days: e.target.value })
                }
              />
            </Grid>

            {/* Status */}
            <Grid item xs={6}>
              <TextField
                select
                fullWidth
                label="Status"
                value={form.status}
                onChange={(e) => setForm({ ...form, status: e.target.value })}
              >
                {["Active", "Completed", "Closed"].map((s) => (
                  <MenuItem key={s} value={s}>
                    {s}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            {/* Notes */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Notes"
                multiline
                rows={3}
                value={form.notes}
                onChange={(e) => setForm({ ...form, notes: e.target.value })}
              />
            </Grid>

            {/* Submit */}
            <Grid item xs={12}>
              <Button type="submit" variant="contained" disabled={loading}>
                {id ? "Update Batch" : "Create Batch"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}
