// src/components/hr/forms/CasualWorkerForm.jsx
import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Grid,
  Paper,
  TextField,
  Typography,
  Snackbar,
  Alert,
} from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import {
  createCasualWorker,
  getCasualWorkerById,
  updateCasualWorker,
} from "../api/hrApi";

export default function CasualWorkerForm() {
  const navigate = useNavigate();
  const { id } = useParams(); // detect edit mode

  const [form, setForm] = useState({
    farm_id: 1, // hardcoded for now
    name: "",
    contact: "",
    skill: "",
    daily_rate: 0,
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  // Load existing worker if editing
  useEffect(() => {
    if (id) {
      setLoading(true);
      getCasualWorkerById(id)
        .then((res) => setForm(res.data))
        .finally(() => setLoading(false));
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (id) {
        await updateCasualWorker(id, form);
      } else {
        await createCasualWorker(form);
      }
      setSuccess(true);
      setTimeout(() => navigate("/hr/casual"), 1000); // redirect after success
    } catch (err) {
      console.error("Error saving casual worker:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        {id ? "Edit Casual Worker" : "New Casual Worker"}
      </Typography>

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Name"
                value={form.name}
                onChange={(e) =>
                  setForm({ ...form, name: e.target.value })
                }
                required
                disabled={loading}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Contact"
                value={form.contact}
                onChange={(e) =>
                  setForm({ ...form, contact: e.target.value })
                }
                disabled={loading}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Skill"
                value={form.skill}
                onChange={(e) =>
                  setForm({ ...form, skill: e.target.value })
                }
                disabled={loading}
              />
            </Grid>

            <Grid item xs={6}>
              <TextField
                fullWidth
                type="number"
                label="Daily Rate"
                value={form.daily_rate}
                onChange={(e) =>
                  setForm({ ...form, daily_rate: Number(e.target.value) })
                }
                disabled={loading}
              />
            </Grid>

            <Grid item xs={12}>
              <Button
                variant="contained"
                type="submit"
                disabled={loading}
              >
                {id ? "Update Casual Worker" : "Save Casual Worker"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>

      {/* Success Snackbar */}
      <Snackbar
        open={success}
        autoHideDuration={2000}
        onClose={() => setSuccess(false)}
      >
        <Alert severity="success" sx={{ width: "100%" }}>
          Casual worker {id ? "updated" : "created"} successfully!
        </Alert>
      </Snackbar>
    </Box>
  );
}
