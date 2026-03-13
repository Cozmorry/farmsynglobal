// src/components/store_inventory/forms/InventoryTransactionForm.jsx

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
  getInventoryTransaction,
  createInventoryTransaction,
  updateInventoryTransaction,
} from "../api/storeInventoryApi";

export default function InventoryTransactionForm() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    item_id: "",
    transaction_type: "IN",
    quantity: 0,
    unit_cost: 0,
  });

  useEffect(() => {
    if (id) {
      getInventoryTransaction(id).then((res) => setForm(res.data));
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (id) await updateInventoryTransaction(id, form);
    else await createInventoryTransaction(form);

    navigate("/store-inventory/transactions");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        {id ? "Edit Transaction" : "New Transaction"}
      </Typography>

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Item ID"
                type="number"
                value={form.item_id}
                onChange={(e) =>
                  setForm({ ...form, item_id: e.target.value })
                }
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                select
                fullWidth
                label="Transaction Type"
                value={form.transaction_type}
                onChange={(e) =>
                  setForm({ ...form, transaction_type: e.target.value })
                }
              >
                {["IN", "OUT", "ADJUSTMENT"].map((t) => (
                  <MenuItem key={t} value={t}>
                    {t}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>

            <Grid item xs={6}>
              <TextField
                fullWidth
                type="number"
                label="Quantity"
                value={form.quantity}
                onChange={(e) =>
                  setForm({ ...form, quantity: e.target.value })
                }
              />
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

            <Grid item xs={12}>
              <Button variant="contained" type="submit">
                {id ? "Update Transaction" : "Create Transaction"}
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
}

