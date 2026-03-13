// src/components/store_inventory/forms/StoreItemForm.jsx

import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Grid,
  MenuItem,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";

import {
  getStoreItem,
  createStoreItem,
  updateStoreItem,
} from "../api/storeInventoryApi";

export default function StoreItemForm() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    category: "General",
    module_type: "General",
    unit_cost: 0,
    quantity_in_stock: 0,
  });

  useEffect(() => {
    if (id) {
      getStoreItem(id).then((res) => setForm(res.data));
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (id) await updateStoreItem(id, form);
    else await createStoreItem(form);
    navigate("/store-inventory/items");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        {id ? "Edit Store Item" : "New Store Item"}
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
              />
            </Grid>

            <Grid item xs={6}>
              <TextField
                select
                fullWidth
                label="Category"
                value={form.category}
                onChange={(e) =>
                  setForm({ ...form, category: e.target.value })
                }
              >
                {[
                  "Seed",
                  "Fertilizer",
                  "Chemical",
                  "Tool",
                  "Machine",
                  "Feed",
                  "Drug",
                  "General",
                ].map((c) => (
                  <MenuItem key={c} value={c}>
                    {c}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            <Grid item xs={6}>
              <TextField
                select
                fullWidth
                label="Module Type"
                value={form.module_type}
                onChange={(e) =>
                  setForm({ ...form, module_type: e.target.value })
                }
              >
                {["Crop", "Livestock", "Poultry", "Aquaculture", "General"].map(
                  (m) => (
                    <MenuItem key={m} value={m}>
                      {m}
                    </MenuItem>
                  )
                )}
              </TextField>
            </Grid>

            <Grid item xs={6}>
              <TextField
                fullWidth
                type="number"
                label="Unit Cost"
                value={form.unit_cost}
                onChange={(e) =>
                  setForm({ ...form, unit_cost: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={6}>
              <TextField
                fullWidth
                type="number"
                label="Quantity In Stock"
                value={form.quantity_in_stock}
                onChange={(e) =>
                  setForm({ ...form, quantity_in_stock: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={12}>
              <Button variant="contained" type="submit">
                {id ? "Update Item" : "Create Item"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}

