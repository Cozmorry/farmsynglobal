// src/components/pages/CropList.jsx
import React, { useState } from "react";
import CropList from "./CropList";
import CropForm from "../forms/CropForm";

const columns = [
  { field: "id", headerName: "ID", width: 70 },

  { field: "name", headerName: "Crop Name", width: 150 },

  { field: "variety", headerName: "Variety", width: 150 },

  {
    field: "planting_date",
    headerName: "Planting Date",
    width: 150,
    valueFormatter: (params) =>
      params.value ? new Date(params.value).toLocaleDateString() : "-",
  },

  {
    field: "season_start",
    headerName: "Season Start",
    width: 150,
    valueFormatter: (params) =>
      params.value ? new Date(params.value).toLocaleDateString() : "-",
  },

  {
    field: "season_end",
    headerName: "Season End",
    width: 150,
    valueFormatter: (params) =>
      params.value ? new Date(params.value).toLocaleDateString() : "-",
  },

  {
    field: "status",
    headerName: "Status",
    width: 120,
  },
];

const CropListPage = () => {
  const [editCrop, setEditCrop] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setEditCrop(null);
    setRefreshKey((prev) => prev + 1);
  };

  // Inject action buttons dynamically
  const enhancedColumns = [
    ...columns,
    {
      field: "actions",
      headerName: "Actions",
      width: 160,
      sortable: false,
      renderCell: (params) => (
        <div>
          <button
            onClick={() => setEditCrop(params.row)}
            style={{ marginRight: 8, color: "blue", cursor: "pointer" }}
          >
            Edit
          </button>

          <button
            onClick={() => console.log("Delete crop", params.row.id)}
            style={{ color: "red", cursor: "pointer" }}
          >
            Delete
          </button>
        </div>
      ),
    },
  ];

  return (
    <div>
      {/* Crop Form (Create / Edit) */}
      {editCrop && (
        <CropForm
          farmId={editCrop.farm_id}
          blockId={editCrop.block_id}
          editData={editCrop}
          onSuccess={handleSuccess}
        />
      )}

      {/* Crop List */}
      <CropList
        key={refreshKey}
        title="Crops"
        endpoint="/api/crop-management/crops/"
        columns={enhancedColumns}
      />
    </div>
  );
};

export default CropListPage;

