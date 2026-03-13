// src/components/pages/CropHarvestList.jsx
import { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";
import { Dialog, DialogTitle, DialogContent } from "@mui/material";

export default function CropHarvestList() {
  const [editRow, setEditRow] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setEditRow(null);
    setRefreshKey((prev) => prev + 1); // trigger list refresh
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    {
      field: "harvest_date",
      headerName: "Harvest Date",
      width: 130,
      valueFormatter: (p) => (p.value ? new Date(p.value).toLocaleDateString() : "-"),
    },
    { field: "field_weight", headerName: "Field Weight (kg)", width: 140, type: "number" },
    { field: "final_weight", headerName: "Final Weight (kg)", width: 140, type: "number" },
    { field: "moisture_content", headerName: "Moisture (%)", width: 120, type: "number" },
    {
      field: "labour_cost",
      headerName: "Labour Cost",
      width: 120,
      type: "number",
      valueFormatter: (p) => (p.value ? `$${p.value.toFixed(2)}` : "-"),
    },
    {
      field: "input_cost",
      headerName: "Input Cost",
      width: 120,
      type: "number",
      valueFormatter: (p) => (p.value ? `$${p.value.toFixed(2)}` : "-"),
    },
    {
      field: "total_cost",
      headerName: "Total Cost",
      width: 120,
      type: "number",
      valueFormatter: (p) => (p.value ? `$${p.value.toFixed(2)}` : "-"),
    },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <div>
          <button
            onClick={() => setEditRow(params.row)}
            style={{ marginRight: 8, color: "blue" }}
          >
            Edit
          </button>
        </div>
      ),
    },
  ];

  return (
    <>
      <CropList
        key={refreshKey}
        title="Crop Harvests"
        endpoint="/api/crop-management/harvests"
        columns={columns}
      />

      <Dialog
        open={!!editRow}
        onClose={() => setEditRow(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>{editRow ? "Edit Crop Harvest" : "New Crop Harvest"}</DialogTitle>
        <DialogContent>
          {editRow && (
            <CropHarvestForm
              cropId={editRow.crop_id}
              blockId={editRow.block_id}
              editData={editRow}
              onSuccess={handleSuccess}
            />
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}


