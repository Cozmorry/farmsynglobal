import React, { useState } from "react";
import { Button, TextField, Paper } from "@mui/material";
import axios from "axios";
import { API_BASE_URL } from "../../../core/config/env";

const ActivityUpload = ({ cropId, activityId, onUploaded }) => {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("crop_id", cropId);
    formData.append("activity_id", activityId);
    formData.append("description", description);

    await axios.post(
      `${API_BASE_URL}/crop_management/uploads/`,
      formData
    );

    setFile(null);
    setDescription("");
    onUploaded && onUploaded();
  };

  return (
    <Paper sx={{ p: 2, mt: 2 }}>
      <TextField
        fullWidth
        label="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        sx={{ mb: 2 }}
      />

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <Button
        sx={{ mt: 2 }}
        variant="contained"
        onClick={handleUpload}
      >
        Upload File
      </Button>
    </Paper>
  );
};

export default ActivityUpload;
