// src/components/pages/CropActivityList.jsx
import { useState } from "react";
import CropList from "./CropList";
import { Dialog, DialogTitle, DialogContent } from "@mui/material";
import SubmoduleForm from "../forms/SubmoduleForm";

export default function CropActivityList() {
  const [editRow, setEditRow] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setEditRow(null);
    setRefreshKey((prev) => prev + 1);
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "activity_type", headerName: "Activity Type", width: 150 },
    { field: "description", headerName: "Description", width: 200 },
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
      field: "date",
      headerName: "Date",
      width: 120,
      valueFormatter: (p) =>
        p.value ? new Date(p.value).toLocaleDateString() : "-",
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
        title="Crop Activities"
        endpoint="/api/crop-management/activities"
        columns={columns}
      />

      <Dialog
        open={!!editRow}
        onClose={() => setEditRow(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {editRow ? "Edit Crop Activity" : "New Crop Activity"}
        </DialogTitle>
        <DialogContent>
          {editRow && (
            <CropActivityForm
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


