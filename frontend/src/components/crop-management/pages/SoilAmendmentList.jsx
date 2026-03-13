// src/components/pages/SoilAmendmentList.jsx
import React, { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

const SoilAmendmentList = () => {
  const [editRow, setEditRow] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setEditRow(null);
    setRefreshKey((prev) => prev + 1);
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },

    { field: "amendment_type", headerName: "Amendment Type", width: 160 },

    { field: "quantity", headerName: "Quantity", width: 120 },

    {
      field: "unit_cost",
      headerName: "Unit Cost",
      width: 120,
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
      field: "date",
      headerName: "Date",
      width: 130,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleDateString() : "-"
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
        <SoilAmendmentForm
          cropId={editRow.crop_id}
          blockId={editRow.block_id}
          editData={editRow}
          onSuccess={handleSuccess}
        />
      )}

      <CropList
        key={refreshKey}
        title="Soil Amendments"
        endpoint="/api/crop-management/soil-amendments"
        columns={columns}
      />
    </div>
  );
};

export default SoilAmendmentList;


