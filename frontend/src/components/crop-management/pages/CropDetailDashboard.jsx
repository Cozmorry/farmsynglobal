// src/components/crop_management/pages/CropDetailDashboard.jsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Button,
} from "@mui/material";
import axios from "axios";
import { API_BASE_URL } from "../../../core/config/env";

// Submodule Table Component
const SubmoduleTable = ({ title, data, columns, addLink, navigate }) => (
  <Paper sx={{ p: 2, mb: 3 }}>
    <Grid container justifyContent="space-between" alignItems="center">
      <Typography variant="h6">{title}</Typography>
      {addLink && (
        <Button variant="contained" onClick={() => navigate(addLink)}>
          Add New
        </Button>
      )}
    </Grid>

    <Table size="small" sx={{ mt: 2 }}>
      <TableHead>
        <TableRow>
          {columns.map((col) => (
            <TableCell key={col.field}>{col.headerName || col.field}</TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {data.length > 0 ? (
          data.map((row) => (
            <TableRow key={row.id}>
              {columns.map((col) => (
                <TableCell key={col.field}>
                  {col.render ? col.render(row[col.field], row) : row[col.field] ?? "-"}
                </TableCell>
              ))}
            </TableRow>
          ))
        ) : (
          <TableRow>
            <TableCell colSpan={columns.length} align="center">
              No records found.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  </Paper>
);

const CropDetailDashboard = () => {
  const { cropId } = useParams();
  const numericCropId = Number(cropId);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [crop, setCrop] = useState(null);
  const [submodules, setSubmodules] = useState({});

  useEffect(() => {
    if (!numericCropId || Number.isNaN(numericCropId)) {
      console.error("Invalid crop ID:", cropId);
      setLoading(false);
      return;
    }
    fetchCropDetail();
  }, [numericCropId]);

  const fetchCropDetail = async () => {
    try {
      const endpoints = {
        crop: `${API_BASE_URL}/crops/${numericCropId}`,
        activities: `${API_BASE_URL}/activities/general-activities/?crop_id=${numericCropId}`,
        harvests: `${API_BASE_URL}/harvests/?crop_id=${numericCropId}`,
        sales: `${API_BASE_URL}/sales/?crop_id=${numericCropId}`,
        landPreparations: `${API_BASE_URL}/activities/land-preparations/?crop_id=${numericCropId}`,
        nursery: `${API_BASE_URL}/activities/nursery-activities/?crop_id=${numericCropId}`,
        fertilizer: `${API_BASE_URL}/activities/fertilizer-applications/?crop_id=${numericCropId}`,
        chemical: `${API_BASE_URL}/activities/chemical-applications/?crop_id=${numericCropId}`,
        weeding: `${API_BASE_URL}/activities/weeding-activities/?crop_id=${numericCropId}`,
        scouting: `${API_BASE_URL}/activities/scouting-activities/?crop_id=${numericCropId}`,
        soilTests: `${API_BASE_URL}/activities/soil-tests/?crop_id=${numericCropId}`,
        soilAmendments: `${API_BASE_URL}/activities/soil-amendments/?crop_id=${numericCropId}`,
        cropRotations: `${API_BASE_URL}/activities/crop-rotations/?crop_id=${numericCropId}`,
      };

      const responses = await Promise.all(
        Object.values(endpoints).map((url) => axios.get(url))
      );

      setCrop(responses[0].data);
      setSubmodules({
        activities: responses[1].data || [],
        harvests: responses[2].data || [],
        sales: responses[3].data || [],
        landPreparations: responses[4].data || [],
        nursery: responses[5].data || [],
        fertilizer: responses[6].data || [],
        chemical: responses[7].data || [],
        weeding: responses[8].data || [],
        scouting: responses[9].data || [],
        soilTests: responses[10].data || [],
        soilAmendments: responses[11].data || [],
        cropRotations: responses[12].data || [],
      });
    } catch (err) {
      console.error("ERROR LOADING CROP DETAIL:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <center style={{ marginTop: 80 }}>
        <CircularProgress />
      </center>
    );
  }

  if (!crop) {
    return (
      <Typography variant="h6" color="error">
        Crop not found.
      </Typography>
    );
  }

  const totalInputCost = submodules.activities?.reduce(
    (acc, a) => acc + (a.input_cost || 0) + (a.labour_cost || 0),
    0
  );
  const totalRevenue = submodules.sales?.reduce((acc, s) => acc + (s.income || 0), 0);
  const totalProfit = totalRevenue - totalInputCost;
  const totalHarvestWeight = submodules.harvests?.reduce((acc, h) => acc + (h.final_weight || 0), 0);

  const submoduleConfig = [
    { key: "activities", title: "General Activities", columns: [{ field: "name" }, { field: "input_cost" }, { field: "labour_cost" }], path: "general-activities/new" },
    { key: "landPreparations", title: "Land Preparations", columns: [{ field: "name" }], path: "land-preparations/new" },
    { key: "nursery", title: "Nursery Activities", columns: [{ field: "name" }], path: "nursery-activities/new" },
    { key: "fertilizer", title: "Fertilizer Applications", columns: [{ field: "fertilizer_type" }, { field: "amount" }], path: "fertilizer-applications/new" },
    { key: "chemical", title: "Chemical Applications", columns: [{ field: "chemical_type" }, { field: "amount" }], path: "chemical-applications/new" },
    { key: "weeding", title: "Weeding Activities", columns: [{ field: "method" }, { field: "date" }], path: "weeding-activities/new" },
    { key: "scouting", title: "Scouting Activities", columns: [{ field: "issue_found" }, { field: "date" }], path: "scouting-activities/new" },
    { key: "soilTests", title: "Soil Tests", columns: [{ field: "test_type" }, { field: "result" }], path: "soil-tests/new" },
    { key: "soilAmendments", title: "Soil Amendments", columns: [{ field: "amendment_type" }, { field: "amount" }], path: "soil-amendments/new" },
    { key: "cropRotations", title: "Crop Rotations", columns: [{ field: "crop_name" }, { field: "rotation_date" }], path: "crop-rotations/new" },
    { key: "harvests", title: "Harvests", columns: [{ field: "final_weight" }, { field: "date" }], path: "harvests/new" },
    { key: "sales", title: "Sales", columns: [{ field: "income" }, { field: "date" }], path: "sales/new" },
  ];

  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>
        {crop.name} — Detail Dashboard
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography>Variety: {crop.variety || "-"}</Typography>
        <Typography>Farm: {crop.farm?.name || "-"}</Typography>
        <Typography>Block: {crop.block?.name || "-"}</Typography>
        <Typography>Planting Date: {crop.planting_date || "-"}</Typography>
        <Typography>
          Season: {crop.season_start || "-"} → {crop.season_end || "-"}
        </Typography>
        <Typography>Status: {crop.status || "-"}</Typography>
      </Paper>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography>Total Input Cost</Typography>
            <Typography variant="h5" color="error">
              ${totalInputCost?.toFixed(2)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography>Total Revenue</Typography>
            <Typography variant="h5" color="success.main">
              ${totalRevenue?.toFixed(2)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography>Profit</Typography>
            <Typography variant="h5" color={totalProfit >= 0 ? "success.main" : "error"}>
              ${totalProfit?.toFixed(2)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography>Total Harvest Weight</Typography>
            <Typography variant="h5">{totalHarvestWeight} kg</Typography>
          </Paper>
        </Grid>
      </Grid>

      <Divider sx={{ mb: 3 }} />

      {submoduleConfig.map((sm) => (
        <SubmoduleTable
          key={sm.key}
          title={sm.title}
          data={submodules[sm.key] || []}
          columns={sm.columns}
          addLink={numericCropId ? `/crop-management/crops/${numericCropId}/${sm.path}` : null}
          navigate={navigate}
        />
      ))}
    </div>
  );
};

export default CropDetailDashboard;
