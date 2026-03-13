// src/components/crop_management/forms/SubmoduleForm.jsx
import { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Grid,
  Paper,
  Typography,
  Alert,
  Snackbar,
} from "@mui/material";

import * as api from "../api/cropManagementApi";

/* ======================================================
   ROUTE PARAM → SUBMODULE KEY MAP
====================================================== */
const ROUTE_TO_SUBMODULE = {
  weeding: "weeding-activities",
  fertilizer: "fertilizer-applications",
  chemical: "chemical-applications",
  nursery: "nursery-activities",
  scouting: "scouting-activities",
  soil_tests: "soil-tests",
  soil_amendments: "soil-amendments",
  crop_rotations: "crop-rotations",
  land_preparations: "land-preparations",
  general_activities: "general-activities",
};

/* ======================================================
   SUBMODULE CONFIG (SINGLE SOURCE OF TRUTH)
====================================================== */
const SUBMODULES = {
  "general-activities": {
    title: "General Activity",
    api: api.generalActivities,
    fields: [
      { name: "activity", label: "Activity", required: true },
      { name: "date", label: "Date", type: "date", required: true },
      { name: "notes", label: "Notes" },
    ],
  },

  "chemical-applications": {
    title: "Chemical Application",
    api: api.chemicalApplications,
    fields: [
      { name: "chemical_name", label: "Chemical Name", required: true },
      { name: "quantity_ltr", label: "Quantity (L)", type: "number" },
      { name: "unit_cost", label: "Unit Cost", type: "number" },
      { name: "total_cost", label: "Total Cost", type: "number", readOnly: true },
      { name: "date", label: "Date", type: "date", required: true },
    ],
    autoCalc: (data) => ({
      total_cost: (data.quantity_ltr || 0) * (data.unit_cost || 0),
    }),
  },

  "fertilizer-applications": {
    title: "Fertilizer Application",
    api: api.fertilizerApplications,
    fields: [
      { name: "fertilizer_type", label: "Type", required: true },
      { name: "amount", label: "Amount", type: "number" },
      { name: "date", label: "Date", type: "date", required: true },
    ],
  },

  "weeding-activities": {
    title: "Weeding",
    api: api.weedingActivities,
    fields: [
      { name: "method", label: "Method" },
      { name: "date", label: "Date", type: "date", required: true },
    ],
  },

  "scouting-activities": {
    title: "Scouting",
    api: api.scoutingActivities,
    fields: [
      { name: "observations", label: "Observations", required: true },
      { name: "date", label: "Date", type: "date", required: true },
    ],
  },

  "soil-tests": {
    title: "Soil Test",
    api: api.soilTests,
    fields: [
      { name: "ph", label: "pH", type: "number" },
      { name: "nutrients", label: "Nutrients" },
      { name: "date", label: "Date", type: "date", required: true },
    ],
  },

  "soil-amendments": {
    title: "Soil Amendment",
    api: api.soilAmendments,
    fields: [
      { name: "amendment", label: "Amendment", required: true },
      { name: "quantity", label: "Quantity", type: "number" },
      { name: "date", label: "Date", type: "date", required: true },
    ],
  },

  "crop-rotations": {
    title: "Crop Rotation",
    api: api.cropRotations,
    fields: [
      { name: "previous_crop", label: "Previous Crop" },
      { name: "next_crop", label: "Next Crop" },
      { name: "date", label: "Date", type: "date", required: true },
    ],
  },

  "land-preparations": {
    title: "Land Preparation",
    api: api.landPreparations,
    fields: [
      { name: "method", label: "Method", required: true },
      { name: "date", label: "Date", type: "date", required: true },
    ],
  },

  "nursery-activities": {
    title: "Nursery Activity",
    api: api.nurseryActivities,
    fields: [
      { name: "activity", label: "Activity", required: true },
      { name: "date", label: "Date", type: "date", required: true },
    ],
  },
};

/* ======================================================
   COMPONENT
====================================================== */
export default function SubmoduleForm({
  submodule,
  cropId,
  blockId,
  editData,
  onSuccess,
}) {
  const resolvedKey = ROUTE_TO_SUBMODULE[submodule] || submodule;
  const config = SUBMODULES[resolvedKey];

  if (!config) {
    return (
      <Alert severity="error">
        Unknown submodule: <strong>{submodule}</strong>
      </Alert>
    );
  }

  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  /* Initialize form */
  useEffect(() => {
    const initial = {};
    config.fields.forEach((f) => {
      initial[f.name] =
        editData?.[f.name] ?? (f.type === "number" ? 0 : "");
    });
    setFormData(initial);
  }, [editData, config]);

  /* Auto calculations (safe) */
  useEffect(() => {
    if (!config.autoCalc) return;
    setFormData((prev) => ({
      ...prev,
      ...config.autoCalc(prev),
    }));
  }, [formData.quantity_ltr, formData.unit_cost]); // intentional deps

  const handleChange = (name, value) =>
    setFormData((prev) => ({ ...prev, [name]: value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (!cropId) {
        throw new Error("Crop ID is missing");
      }

      const payload = {
        ...formData,
        crop_id: cropId,
        block_id: blockId ?? null,
      };

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

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        {editData ? `Edit ${config.title}` : `New ${config.title}`}
      </Typography>

      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          {config.fields.map((f) => (
            <Grid item xs={12} md={6} key={f.name}>
              <TextField
                label={f.label}
                type={f.type || "text"}
                fullWidth
                required={f.required}
                value={formData[f.name] ?? ""}
                onChange={(e) =>
                  handleChange(
                    f.name,
                    f.type === "number"
                      ? Number(e.target.value)
                      : e.target.value
                  )
                }
                InputProps={f.readOnly ? { readOnly: true } : {}}
              />
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
        <Alert severity="success">{config.title} saved successfully</Alert>
      </Snackbar>
    </Paper>
  );
}
