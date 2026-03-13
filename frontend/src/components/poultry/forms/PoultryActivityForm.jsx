// src/components/poultry/forms/PoultryActivityForm.jsx

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
  getActivity,
  createActivity,
  updateActivity,
  getBatches,
} from "../api/poultryApi";
import { normalizeDate, number } from "./utils";

export default function PoultryActivityForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [batches, setBatches] = useState([]);

  const [form, setForm] = useState({
    batch_id: "",
    activity_type: "FEED",
    date: "",
    notes: "",
  });

  /* Load batches */
  useEffect(() => {
    getBatches().then((res) => setBatches(res.data || []));
  }, []);

  /* Load activity if editing */
  useEffect(() => {
    if (!id) return;

    getActivity(id).then((res) =>
      setForm({
        ...res.data,
        batch_id: number(res.data.batch_id),
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
    };

    if (id) await updateActivity(id, payload);
    else await createActivity(payload);

    navigate("/poultry/activities");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} mb={3}>
        {id ? "Edit Activity" : "New Activity"}
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

            {/* Activity Type */}
            <Grid item xs={6}>
              <TextField
                select
                fullWidth
                label="Activity Type"
                value={form.activity_type}
                onChange={(e) =>
                  setForm({ ...form, activity_type: e.target.value })
                }
              >
                {["FEED", "VACCINE", "MEDICATION", "WATER"].map((t) => (
                  <MenuItem key={t} value={t}>
                    {t}
                  </MenuItem>
                ))}
              </TextField>
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

            {/* Notes */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Notes"
                value={form.notes}
                onChange={(e) =>
                  setForm({ ...form, notes: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={12}>
              <Button type="submit" variant="contained" disabled={loading}>
                {id ? "Update Activity" : "Create Activity"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}
