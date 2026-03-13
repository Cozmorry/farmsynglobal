// src/components/pages/CropRotationList.jsx
import { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";
import { Dialog, DialogTitle, DialogContent } from "@mui/material";

export default function CropRotationList() {
  const [editRow, setEditRow] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setEditRow(null);
    setRefreshKey((prev) => prev + 1);
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "previous_crop", headerName: "Previous Crop", width: 160 },
    { field: "next_crop", headerName: "Next Crop", width: 160 },
    {
      field: "rotation_start",
      headerName: "Rotation Start",
      width: 130,
      valueFormatter: (p) => (p.value ? new Date(p.value).toLocaleDateString() : "-"),
    },
    {
      field: "rotation_end",
      headerName: "Rotation End",
      width: 130,
      valueFormatter: (p) => (p.value ? new Date(p.value).toLocaleDateString() : "-"),
    },
    { field: "notes", headerName: "Notes", width: 200 },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <div>
          <button
            onClick={() => setEditRow(params.row)}
            style={{ marginRight: 8, color: "blue", cursor: "pointer" }}
          >
            Edit
          </button>
          <button
            onClick={() => console.log("Delete", params.row.id)}
            style={{ color: "red", cursor: "pointer" }}
          >
            Delete
          </button>
        </div>
      ),
    },
  ];

  return (
    <>
      <CropList
        key={refreshKey}
        title="Crop Rotations"
        endpoint="/api/crop-management/crop-rotations"
        columns={columns}
      />

      <Dialog
        open={!!editRow}
        onClose={() => setEditRow(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>{editRow ? "Edit Crop Rotation" : "New Crop Rotation"}</DialogTitle>
        <DialogContent>
          {editRow && (
            <CropRotationForm
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

