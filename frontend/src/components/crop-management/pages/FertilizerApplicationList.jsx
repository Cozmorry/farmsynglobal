// src/components/pages/FertilizerApplicationList.jsx
import { useState } from "react";
import { Dialog, DialogTitle, DialogContent, Button } from "@mui/material";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

export default function FertilizerApplicationList({ cropId }) {
  const [editRow, setEditRow] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [openNew, setOpenNew] = useState(false);

  const handleSuccess = () => {
    setEditRow(null);
    setOpenNew(false);
    setRefreshKey((prev) => prev + 1);
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },
    {
      field: "application_date",
      headerName: "Application Date",
      width: 130,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleDateString() : "-",
    },
    { field: "fertilizer_type", headerName: "Fertilizer Type", width: 180 },
    {
      field: "quantity_applied",
      headerName: "Quantity Applied (kg)",
      width: 160,
      type: "number",
    },
    {
      field: "cost",
      headerName: "Cost",
      width: 120,
      type: "number",
      valueFormatter: (params) => (params.value ? `$${params.value.toFixed(2)}` : "-"),
    },
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <Button variant="text" onClick={() => setEditRow(params.row)}>
          Edit
        </Button>
      ),
    },
  ];

  return (
    <>
      <div style={{ marginBottom: 16 }}>
        <Button variant="contained" onClick={() => setOpenNew(true)}>
          Add Fertilizer Application
        </Button>
      </div>

      <CropList
        key={refreshKey}
        title="Fertilizer Applications"
        endpoint="/api/crop-management/fertilizer-applications"
        columns={columns}
      />

      {/* Dialog for editing */}
      <Dialog open={!!editRow} onClose={() => setEditRow(null)} maxWidth="md" fullWidth>
        <DialogTitle>Edit Fertilizer Application</DialogTitle>
        <DialogContent>
          {editRow && (
            <SubmoduleForm
              type="fertilizerApplication"
              cropId={editRow.crop_id}
              blockId={editRow.block_id}
              editData={editRow}
              onSuccess={handleSuccess}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Dialog for adding new */}
      <Dialog open={openNew} onClose={() => setOpenNew(false)} maxWidth="md" fullWidth>
        <DialogTitle>New Fertilizer Application</DialogTitle>
        <DialogContent>
          <SubmoduleForm type="fertilizerApplication" cropId={cropId} onSuccess={handleSuccess} />
        </DialogContent>
      </Dialog>
    </>
  );
}
