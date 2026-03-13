// src/components/livestock/forms/LivestockForm.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, TextField, MenuItem, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import { livestock } from "../api/LivestockApi";

export default function LivestockForm() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [form, setForm] = useState({
    name: "",
    tag_number: "",
    type: "Cattle",
    breed: "",
    gender: "Male",
    status: "active",
    remarks: "",
  });

  const types = ["Cattle", "Sheep", "Goat", "Pig", "Other"];
  const genders = ["Male", "Female"];
  const statuses = ["active", "sold", "slaughtered", "deceased"];

  useEffect(() => {
    if (id) {
      livestock.get(id).then((res) => {
        setForm(res.data);
      });
    }
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (id) {
        await livestock.update(id, form);
      } else {
        await livestock.create(form);
      }
      navigate("/livestock/animals");
    } catch (error) {
      console.error("Failed to save livestock:", error);
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        {id ? "Edit Animal" : "Add Animal"}
      </Typography>

      <form onSubmit={handleSubmit}>
        <TextField
          label="Name"
          name="name"
          value={form.name}
          onChange={handleChange}
          fullWidth
          required
          sx={{ mb: 2 }}
        />

        <TextField
          label="Tag Number"
          name="tag_number"
          value={form.tag_number}
          onChange={handleChange}
          fullWidth
          required
          sx={{ mb: 2 }}
        />

        <TextField
          label="Type"
          name="type"
          value={form.type}
          onChange={handleChange}
          select
          fullWidth
          sx={{ mb: 2 }}
        >
          {types.map((t) => (
            <MenuItem key={t} value={t}>
              {t}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="Gender"
          name="gender"
          value={form.gender}
          onChange={handleChange}
          select
          fullWidth
          sx={{ mb: 2 }}
        >
          {genders.map((g) => (
            <MenuItem key={g} value={g}>
              {g}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="Status"
          name="status"
          value={form.status}
          onChange={handleChange}
          select
          fullWidth
          sx={{ mb: 2 }}
        >
          {statuses.map((s) => (
            <MenuItem key={s} value={s}>
              {s}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="Remarks"
          name="remarks"
          value={form.remarks}
          onChange={handleChange}
          fullWidth
          multiline
          rows={3}
          sx={{ mb: 3 }}
        />

        <Button type="submit" variant="contained">
          {id ? "Update" : "Create"}
        </Button>
      </form>
    </Box>
  );
}
