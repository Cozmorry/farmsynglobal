// src/components/livestock/forms/LivestockGroupForm.jsx
import React, { useState } from "react";
import { Box, Button, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { groups } from "../api/livestockApi";

export default function LivestockGroupForm() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    description: "",
    farm_id: 1,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await groups.create(form);
      navigate("/livestock/groups");
    } catch (error) {
      console.error("Failed to create livestock group:", error);
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Add Group
      </Typography>

      <form onSubmit={handleSubmit}>
        <TextField
          label="Group Name"
          name="name"
          value={form.name}
          onChange={handleChange}
          fullWidth
          required
          sx={{ mb: 2 }}
        />

        <TextField
          label="Description"
          name="description"
          value={form.description}
          onChange={handleChange}
          fullWidth
          multiline
          rows={3}
          sx={{ mb: 3 }}
        />

        <Button type="submit" variant="contained">
          Create
        </Button>
      </form>
    </Box>
  );
}
