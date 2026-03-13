// src/components/pages/SoilTestList.jsx
import React, { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

const SoilTestList = () => {
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
      headerName: "Test Date",
      width: 130,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleDateString() : "-"
    },

    { field: "ph", headerName: "pH", width: 90 },
    { field: "ec", headerName: "EC", width: 90 },
    { field: "n", headerName: "Nitrogen (N)", width: 150 },
    { field: "p", headerName: "Phosphorus (P)", width: 150 },
    { field: "k", headerName: "Potassium (K)", width: 150 },

    { field: "micronutrients", headerName: "Micronutrients", width: 200 },

    {
      field: "lab_report",
      headerName: "Lab Report",
      width: 200,
      renderCell: (params) =>
        params.value ? (
          <a href={params.value} target="_blank" rel="noopener noreferrer">
            View Report
          </a>
        ) : "-"
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
        <SoilTestForm
          cropId={editRow.crop_id}
          blockId={editRow.block_id}
          editData={editRow}
          onSuccess={handleSuccess}
        />
      )}

      <CropList
        key={refreshKey}
        title="Soil Test Records"
        endpoint="/api/crop-management/soil-tests"
        columns={columns}
      />
    </div>
  );
};

export default SoilTestList;


