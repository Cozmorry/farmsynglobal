// src/components/hr/forms/PermanentStaffForm.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Grid, Paper, TextField, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import { createPermanentStaff, getPermanentStaffById, updatePermanentStaff } from "../api/hrApi";

export default function PermanentStaffForm() {
  const navigate = useNavigate();
  const { id } = useParams(); // used for edit

  const [form, setForm] = useState({
    farm_id: 1,
    name: "",
    contact: "",
    position: "",
    salary: 0,
  });

  useEffect(() => {
    if (id) {
      // fetch existing staff data
      getPermanentStaffById(id).then((res) => {
        if (res.data && res.data.length > 0) setForm(res.data[0]);
      });
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (id) {
      await updatePermanentStaff(id, form);
    } else {
      await createPermanentStaff(form);
    }
    navigate("/hr/permanent");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        {id ? "Edit Permanent Staff" : "New Permanent Staff"}
      </Typography>

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Name"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Contact"
                value={form.contact}
                onChange={(e) => setForm({ ...form, contact: e.target.value })}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Position"
                value={form.position}
                onChange={(e) => setForm({ ...form, position: e.target.value })}
              />
            </Grid>

            <Grid item xs={6}>
              <TextField
                fullWidth
                type="number"
                label="Salary"
                value={form.salary}
                onChange={(e) => setForm({ ...form, salary: e.target.value })}
              />
            </Grid>

            <Grid item xs={12}>
              <Button variant="contained" type="submit">
                {id ? "Update Staff" : "Save Staff"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}
