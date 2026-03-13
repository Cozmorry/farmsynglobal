// src/components/livestock/pages/LivestockList.jsx
import React, { useEffect, useState } from "react";
import { Box, Button, Typography, Paper } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { livestock } from "../api/LivestockApi";

export default function LivestockList() {
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    livestock.list().then((res) => setRows(res.data));
  }, []);

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "name", headerName: "Name", width: 150 },
    { field: "tag_number", headerName: "Tag Number", width: 120 },
    { field: "type", headerName: "Type", width: 100 },
    { field: "gender", headerName: "Gender", width: 100 },
    { field: "status", headerName: "Status", width: 120 },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button
          size="small"
          variant="outlined"
          onClick={() =>
            navigate(`/livestock/animals/edit/${params.row.id}`)
          }
        >
          Edit
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Livestock
      </Typography>

      <Button
        variant="contained"
        sx={{ mb: 2 }}
        onClick={() => navigate("/livestock/animals/new")}
      >
        Add Animal
      </Button>

      <Paper sx={{ height: 600 }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} />
      </Paper>
    </Box>
  );
}




