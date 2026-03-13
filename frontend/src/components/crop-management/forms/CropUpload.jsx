import { useState } from "react";
import { TextField, Button, Grid, Paper, Typography, Snackbar, Alert } from "@mui/material";
import { uploadActivityFile } from "../api/cropManagementApi";

export default function CropActivityUploadForm({ cropId, activityType, activityId, onSuccess, editData }) {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState(editData?.description || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file && !editData) {
      setError("Please select a file to upload.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("crop_id", cropId);
      formData.append("activity_type", activityType);
      formData.append("activity_id", activityId);
      if (file) formData.append("file", file);
      formData.append("description", description);

      await activityFile.upload(formData, editData?.id);
      setSuccess(true);
      onSuccess && onSuccess();
    } catch (err) {
      console.error(err);
      setError("Failed to upload file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3, mt: 2 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        {editData ? "Edit Activity Upload" : "Upload Activity File"}
      </Typography>

      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          {!editData && (
            <Grid item xs={12}>
              <Button variant="contained" component="label">
                Select File
                <input type="file" hidden onChange={(e) => setFile(e.target.files[0])} />
              </Button>
              {file && <Typography sx={{ mt: 1 }}>{file.name}</Typography>}
            </Grid>
          )}

          <Grid item xs={12}>
            <TextField
              label="Description"
              fullWidth
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </Grid>

          {error && (
            <Grid item xs={12}>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}

          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary" disabled={loading}>
              {loading ? "Uploading..." : "Upload File"}
            </Button>
          </Grid>
        </Grid>
      </form>

      <Snackbar open={success} autoHideDuration={3000} onClose={() => setSuccess(false)} anchorOrigin={{ vertical: "bottom", horizontal: "center" }}>
        <Alert onClose={() => setSuccess(false)} severity="success" sx={{ width: "100%" }}>
          File uploaded successfully!
        </Alert>
      </Snackbar>
    </Paper>
  );
}
