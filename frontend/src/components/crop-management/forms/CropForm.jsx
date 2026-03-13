// src/components/forms/CropForm.jsx
import { useState } from "react";
import {
  TextField,
  Button,
  Grid,
  Paper,
  Typography,
  Snackbar,
  Alert,
} from "@mui/material";

import { createCrop, updateCrop } from "../api/cropManagementApi";

export default function CropForm({ farmId, blockId, onSuccess, editData }) {
  const [name, setName] = useState(editData?.name || "");
  const [variety, setVariety] = useState(editData?.variety || "");
  const [plantingDate, setPlantingDate] = useState(
    editData?.planting_date || ""
  );
  const [seasonStart, setSeasonStart] = useState(
    editData?.season_start || ""
  );
  const [seasonEnd, setSeasonEnd] = useState(editData?.season_end || "");
  const [status, setStatus] = useState(editData?.status || "Active");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const payload = {
        farm_id: farmId,
        block_id: blockId,
        name,
        variety,
        planting_date: plantingDate,
        season_start: seasonStart,
        season_end: seasonEnd,
        status,
      };

      if (editData) {
        await crop.update(editData.id, payload);
      } else {
        await crop.create(payload);
      }

      setSuccess(true);
      onSuccess && onSuccess();
    } catch (err) {
      console.error(err);
      setError("Failed to save crop.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3, mt: 2 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        {editData ? "Edit Crop" : "New Crop"}
      </Typography>

      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              label="Crop Name"
              fullWidth
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Variety"
              fullWidth
              value={variety}
              onChange={(e) => setVariety(e.target.value)}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Planting Date"
              type="date"
              fullWidth
              required
              value={plantingDate}
              onChange={(e) => setPlantingDate(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Season Start"
              type="date"
              fullWidth
              value={seasonStart}
              onChange={(e) => setSeasonStart(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Season End"
              type="date"
              fullWidth
              value={seasonEnd}
              onChange={(e) => setSeasonEnd(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              label="Status"
              fullWidth
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            />
          </Grid>

          {error && (
            <Grid item xs={12}>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}

          <Grid item xs={12}>
            <Button type="submit" variant="contained" disabled={loading}>
              {loading ? "Saving..." : "Save Crop"}
            </Button>
          </Grid>
        </Grid>
      </form>

      <Snackbar
        open={success}
        autoHideDuration={3000}
        onClose={() => setSuccess(false)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          severity="success"
          onClose={() => setSuccess(false)}
          sx={{ width: "100%" }}
        >
          Crop saved successfully!
        </Alert>
      </Snackbar>
    </Paper>
  );
}
