// src/components/livestock/forms/LivestockSubmoduleForm.jsx
import { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Grid,
  Paper,
  Typography,
  Alert,
  Snackbar,
  MenuItem,
} from "@mui/material";

import * as api from "../api/livestockApi";
import { useParams } from "react-router-dom";

/* ======================================================
   ROUTE → SUBMODULE MAP
====================================================== */
const ROUTE_TO_SUBMODULE = {
  productions: "production",
  feeding: "feeding",
  activities: "activity",
  expenses: "expense",
  sales: "sale",
  weights: "weight",
};

/* ======================================================
   SUBMODULE CONFIG
====================================================== */
const SUBMODULES = {
  production: {
    title: "Production Record",
    api: api.productions,
    fields: [
      { name: "livestock_id", label: "Livestock ID", type: "number", required: true },
      {
        name: "production_type",
        label: "Production Type",
        type: "select",
        options: ["Milk", "Meat", "Manure", "Generic"],
        required: true,
      },
      { name: "quantity", label: "Quantity", type: "number", required: true },
      { name: "unit_price", label: "Unit Price", type: "number" },
      { name: "total_value", label: "Total Value", type: "number", readOnly: true },
      { name: "fat_content", label: "Fat Content", type: "number" },
      { name: "carcass_weight", label: "Carcass Weight", type: "number" },
      { name: "remarks", label: "Remarks" },
    ],
    autoCalc: (data) => ({
      total_value: (Number(data.quantity) || 0) * (Number(data.unit_price) || 0),
    }),
  },

  feeding: {
    title: "Feeding Record",
    api: api.feedings,
    fields: [
      { name: "livestock_id", label: "Livestock ID", type: "number" },
      { name: "group_id", label: "Group ID", type: "number" },
      { name: "feed_item_id", label: "Feed Item", type: "number", required: true },
      { name: "quantity", label: "Quantity", type: "number", required: true },
      { name: "unit_cost", label: "Unit Cost", type: "number", required: true },
      { name: "total_cost", label: "Total Cost", type: "number", readOnly: true },
      {
        name: "feeding_method",
        label: "Feeding Method",
        type: "select",
        options: ["pasture", "stall", "mixed"],
        required: true,
      },
      { name: "feeding_date", label: "Date", type: "date" },
      { name: "remarks", label: "Remarks" },
    ],
    autoCalc: (data) => ({
      total_cost: (Number(data.quantity) || 0) * (Number(data.unit_cost) || 0),
    }),
  },

  activity: {
    title: "Activity Record",
    api: api.activities,
    fields: [
      { name: "livestock_id", label: "Livestock ID", type: "number" },
      { name: "group_id", label: "Group ID", type: "number" },
      { name: "name", label: "Activity Name", required: true },
      {
        name: "activity_type",
        label: "Activity Type",
        type: "select",
        options: ["service", "consumable"],
        required: true,
      },
      {
        name: "activity_category",
        label: "Category",
        type: "select",
        options: ["health", "breeding", "management"],
        required: true,
      },
      { name: "performed_by", label: "Performed By" },
      { name: "store_item_id", label: "Store Item ID", type: "number" },
      { name: "quantity_used", label: "Quantity Used", type: "number" },
      { name: "unit_cost", label: "Unit Cost", type: "number" },
      { name: "total_cost", label: "Total Cost", type: "number", readOnly: true },
      { name: "date_performed", label: "Date", type: "date" },
      { name: "remarks", label: "Remarks" },
    ],
    autoCalc: (data) => ({
      total_cost: (Number(data.quantity_used) || 0) * (Number(data.unit_cost) || 0),
    }),
  },

  expense: {
    title: "Expense Record",
    api: api.expenses,
    fields: [
      { name: "livestock_id", label: "Livestock ID", type: "number", required: true },
      { name: "category", label: "Category", required: true },
      { name: "sub_category", label: "Sub-category" },
      { name: "amount", label: "Amount", type: "number", required: true },
      { name: "remarks", label: "Remarks" },
    ],
  },

  sale: {
    title: "Sale Record",
    api: api.sales,
    fields: [
      { name: "livestock_id", label: "Livestock ID", type: "number", required: true },
      { name: "production_id", label: "Production ID", type: "number" },
      {
        name: "production_type",
        label: "Production Type",
        type: "select",
        options: ["Milk", "Meat", "Manure", "Generic"],
      },
      { name: "quantity", label: "Quantity", type: "number", required: true },
      { name: "unit_price", label: "Unit Price", type: "number", required: true },
      { name: "total_sale", label: "Total Sale", type: "number", readOnly: true },
      { name: "buyer_name", label: "Buyer" },
      { name: "date", label: "Date", type: "date" },
    ],
    autoCalc: (data) => ({
      total_sale: (Number(data.quantity) || 0) * (Number(data.unit_price) || 0),
    }),
  },

  weight: {
    title: "Weight Record",
    api: api.weights,
    fields: [
      { name: "livestock_id", label: "Livestock ID", type: "number", required: true },
      { name: "weight", label: "Weight", type: "number", required: true },
      { name: "date_recorded", label: "Date", type: "date" },
    ],
  },
};

/* ======================================================
   COMPONENT
====================================================== */
export default function LivestockSubmoduleForm({ editData, onSuccess }) {
  const { submodule } = useParams();
  const resolvedKey = ROUTE_TO_SUBMODULE[submodule] || submodule;
  const config = SUBMODULES[resolvedKey];

  if (!config) {
    return (
      <Alert severity="error">
        Unknown livestock submodule: <strong>{submodule}</strong>
      </Alert>
    );
  }

  /* ======================
     STATE
  ====================== */
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  /* ======================
     INITIALIZE FORM
  ====================== */
  useEffect(() => {
    const initial = {};
    config.fields.forEach((f) => {
      if (editData?.[f.name] !== undefined && editData?.[f.name] !== null) {
        initial[f.name] = editData[f.name];
      } else if (f.type === "number") {
        initial[f.name] = 0;
      } else {
        initial[f.name] = "";
      }
    });
    setFormData(initial);
  }, [editData, config]);

  /* ======================
     AUTO-CALCULATION
     Updates when relevant fields change
  ====================== */
  useEffect(() => {
    if (!config.autoCalc) return;

    setFormData((prev) => {
      const calculated = config.autoCalc(prev);
      const changed = Object.keys(calculated).some(
        (k) => calculated[k] !== prev[k]
      );
      return changed ? { ...prev, ...calculated } : prev;
    });
  }, [formData, config]);

  /* ======================
     HANDLE CHANGE
  ====================== */
  const handleChange = (name, value) =>
    setFormData((prev) => ({ ...prev, [name]: value }));

  /* ======================
     SUBMIT
  ====================== */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const payload = { ...formData };

      if (editData?.id) {
        await config.api.update(editData.id, payload);
      } else {
        await config.api.create(payload);
      }

      setSuccess(true);
      onSuccess?.();
    } catch (err) {
      console.error(err);
      setError(`Failed to save ${config.title}`);
    } finally {
      setLoading(false);
    }
  };

  /* ======================
     RENDER
  ====================== */
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        {editData ? `Edit ${config.title}` : `New ${config.title}`}
      </Typography>

      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          {config.fields.map((f) => (
            <Grid item xs={12} md={6} key={f.name}>
              {f.type === "select" ? (
                <TextField
                  select
                  label={f.label}
                  fullWidth
                  required={f.required}
                  value={formData[f.name]}
                  onChange={(e) => handleChange(f.name, e.target.value)}
                >
                  {f.options.map((opt) => (
                    <MenuItem key={opt} value={opt}>
                      {opt}
                    </MenuItem>
                  ))}
                </TextField>
              ) : (
                <TextField
                  label={f.label}
                  type={f.type || "text"}
                  fullWidth
                  required={f.required}
                  value={formData[f.name]}
                  onChange={(e) =>
                    handleChange(
                      f.name,
                      f.type === "number" ? Number(e.target.value) : e.target.value
                    )
                  }
                  disabled={f.readOnly}
                  InputLabelProps={f.type === "date" ? { shrink: true } : undefined}
                />
              )}
            </Grid>
          ))}

          {error && (
            <Grid item xs={12}>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}

          <Grid item xs={12}>
            <Button type="submit" variant="contained" disabled={loading}>
              {loading ? "Saving..." : `Save ${config.title}`}
            </Button>
          </Grid>
        </Grid>
      </form>

      <Snackbar
        open={success}
        autoHideDuration={3000}
        onClose={() => setSuccess(false)}
      >
        <Alert severity="success" onClose={() => setSuccess(false)}>
          {config.title} saved successfully
        </Alert>
      </Snackbar>
    </Paper>
  );
}

