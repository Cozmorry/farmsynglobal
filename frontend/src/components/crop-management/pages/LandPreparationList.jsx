// src/components/pages/LandPreparationList.jsx
import React, { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

const LandPreparationList = () => {
  const [editRow, setEditRow] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setEditRow(null);
    setRefreshKey((prev) => prev + 1);
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },

    {
      field: "date",
      headerName: "Date",
      width: 140,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleDateString() : "-"
    },

    { field: "method", headerName: "Method", width: 180 },

    {
      field: "cost",
      headerName: "Cost",
      width: 120,
      type: "number",
      valueFormatter: (params) =>
        params.value ? `$${params.value.toFixed(2)}` : "-"
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
          <button
            onClick={() => console.log("Delete", params.row.id)}
            style={{ color: "red" }}
          >
            Delete
          </button>
        </div>
      )
    }
  ];

  return (
    <div>
      {editRow && (
        <LandPreparationForm
          cropId={editRow.crop_id}
          blockId={editRow.block_id}
          editData={editRow}
          onSuccess={handleSuccess}
        />
      )}

      <CropList
        key={refreshKey}
        title="Land Preparations"
        endpoint="/api/crop-management/land-preparation"
        columns={columns}
      />
    </div>
  );
};

export default LandPreparationList;



