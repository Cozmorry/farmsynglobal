// src/components/pages/ChemicalApplicationList.jsx
import { useState } from "react";
import { Dialog, DialogTitle, DialogContent, Button } from "@mui/material";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

export default function ChemicalApplicationList({ cropId }) {
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
    { field: "chemical_name", headerName: "Chemical Name", width: 150 },
    { field: "quantity_ltr", headerName: "Quantity (L)", width: 120, type: "number" },
    { field: "unit_cost", headerName: "Unit Cost", width: 120, type: "number" },
    { field: "total_cost", headerName: "Total Cost", width: 120, type: "number" },
    { field: "date", headerName: "Date", width: 120, 
      valueFormatter: (p) => p.value ? new Date(p.value).toLocaleDateString() : "-" 
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
          Add Chemical Application
        </Button>
      </div>

      <CropList
        key={refreshKey}
        title="Chemical Applications"
        endpoint="/api/crop-management/chemical-applications"
        columns={columns}
      />

      {/* Dialog for editing */}
      <Dialog
        open={!!editRow}
        onClose={() => setEditRow(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Edit Chemical Application</DialogTitle>
        <DialogContent>
          {editRow && (
            <SubmoduleForm
              type="chemicalApplication"
              cropId={editRow.crop_id}
              blockId={editRow.block_id}
              editData={editRow}
              onSuccess={handleSuccess}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Dialog for adding new */}
      <Dialog
        open={openNew}
        onClose={() => setOpenNew(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>New Chemical Application</DialogTitle>
        <DialogContent>
          <SubmoduleForm
            type="chemicalApplication"
            cropId={cropId}
            onSuccess={handleSuccess}
          />
        </DialogContent>
      </Dialog>
    </>
  );
}
