// src/components/poultry/forms/PoultrySaleForm.jsx

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
  getSale,
  createSale,
  updateSale,
  getBatches,
} from "../api/poultryApi";
import { normalizeDate, number } from "./utils";

export default function PoultrySaleForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [batches, setBatches] = useState([]);

  const [form, setForm] = useState({
    batch_id: "",
    product_type: "EGGS",
    quantity: "",
    price: "",
    date: "",
  });

  /* Load batches */
  useEffect(() => {
    getBatches().then((res) => setBatches(res.data || []));
  }, []);

  /* Load sale if editing */
  useEffect(() => {
    if (!id) return;

    getSale(id).then((res) =>
      setForm({
        ...res.data,
        batch_id: number(res.data.batch_id),
        quantity: number(res.data.quantity),
        price: number(res.data.price),
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
      price: number(form.price),
    };

    if (id) await updateSale(id, payload);
    else await createSale(payload);

    navigate("/poultry/sales");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} mb={3}>
        {id ? "Edit Sale" : "New Sale"}
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

            {/* Product Type */}
            <Grid item xs={6}>
              <TextField
                select
                fullWidth
                label="Product Type"
                value={form.product_type}
                onChange={(e) =>
                  setForm({ ...form, product_type: e.target.value })
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

            {/* Price */}
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Price"
                type="number"
                value={form.price}
                onChange={(e) =>
                  setForm({ ...form, price: e.target.value })
                }
                required
              />
            </Grid>

            {/* Date */}
            <Grid item xs={12}>
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
                {id ? "Update Sale" : "Create Sale"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}
