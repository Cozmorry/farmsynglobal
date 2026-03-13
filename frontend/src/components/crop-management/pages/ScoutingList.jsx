// src/components/pages/ScoutingList.jsx
import React, { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

const ScoutingList = () => {
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

    { field: "pests", headerName: "Pests Observed", width: 180 },
    { field: "diseases", headerName: "Diseases Observed", width: 180 },
    { field: "nutrient_deficiency", headerName: "Nutrient Deficiency", width: 180 },
    { field: "notes", headerName: "Notes", width: 200 },

    {
      field: "labour_cost",
      headerName: "Labour Cost",
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
        <ScoutingForm
          cropId={editRow.crop_id}
          blockId={editRow.block_id}
          editData={editRow}
          onSuccess={handleSuccess}
        />
      )}

      <CropList
        key={refreshKey}
        title="Scouting Records"
        endpoint="/api/crop-management/scouting-activities"
        columns={columns}
      />
    </div>
  );
};

export default ScoutingList;


