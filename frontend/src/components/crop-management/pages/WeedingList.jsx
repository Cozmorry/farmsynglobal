// src/components/pages/WeedingList.jsx
import React, { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

const WeedingList = () => {
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
      width: 120,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleDateString() : "-"
    },

    { field: "method", headerName: "Method", width: 150 },

    {
      field: "labour_cost",
      headerName: "Labour Cost",
      width: 130,
      valueFormatter: (params) =>
        params.value ? `$${params.value.toFixed(2)}` : "-"
    },

    {
      field: "input_cost",
      headerName: "Input Cost",
      width: 130,
      valueFormatter: (params) =>
        params.value ? `$${params.value.toFixed(2)}` : "-"
    },

    {
      field: "total_cost",
      headerName: "Total Cost",
      width: 130,
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
        <WeedingForm
          cropId={editRow.crop_id}
          blockId={editRow.block_id}
          editData={editRow}
          onSuccess={handleSuccess}
        />
      )}

      <CropList
        key={refreshKey}
        title="Weeding Activities"
        endpoint="/api/crop-management/weeding-activities"
        columns={columns}
      />
    </div>
  );
};

export default WeedingList;

