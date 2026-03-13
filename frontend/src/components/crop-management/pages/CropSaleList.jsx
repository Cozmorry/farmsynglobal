// src/components/pages/CropSaleList.jsx
import React, { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

const CropSaleList = () => {
  const [editRow, setEditRow] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setEditRow(null);
    setRefreshKey((prev) => prev + 1);
  };

  const columns = [
    { field: "id", headerName: "ID", width: 70 },

    {
      field: "sale_date",
      headerName: "Sale Date",
      width: 130,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleDateString() : "-"
    },

    { field: "buyer", headerName: "Buyer", width: 180 },

    {
      field: "quantity_sold",
      headerName: "Quantity Sold",
      width: 160,
      type: "number"
    },

    {
      field: "unit_price",
      headerName: "Unit Price",
      width: 120,
      type: "number",
      valueFormatter: (params) =>
        params.value ? `$${params.value.toFixed(2)}` : "-"
    },

    {
      field: "total_income",
      headerName: "Total Income",
      width: 140,
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
      ),
    },
  ];

  return (
    <div>
      {editRow && (
        <CropSaleForm
          cropId={editRow.crop_id}
          blockId={editRow.block_id}
          editData={editRow}
          onSuccess={handleSuccess}
        />
      )}

      <CropList
        key={refreshKey}
        title="Crop Sales"
        endpoint="/api/crop-management/sales"
        columns={columns}
      />
    </div>
  );
};

export default CropSaleList;


