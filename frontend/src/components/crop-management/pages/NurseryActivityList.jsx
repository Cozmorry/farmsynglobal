// src/components/pages/NurseryActivityList.jsx
import React, { useState } from "react";
import CropList from "./CropList";
import SubmoduleForm from "../forms/SubmoduleForm";

const baseColumns = [
  { field: "id", headerName: "ID", width: 70 },

  {
    field: "planted_date",
    headerName: "Planted Date",
    width: 130,
    valueFormatter: (p) =>
      p.value ? new Date(p.value).toLocaleDateString() : "-",
  },

  {
    field: "germination_rate",
    headerName: "Germination Rate (%)",
    width: 170,
  },

  { field: "materials_used", headerName: "Materials Used", width: 180 },

  {
    field: "tentative_transplant_date",
    headerName: "Transplant Date",
    width: 160,
    valueFormatter: (p) =>
      p.value ? new Date(p.value).toLocaleDateString() : "-",
  },

  { field: "labour_cost", headerName: "Labour Cost", width: 120 },
  { field: "chemicals_cost", headerName: "Chemicals Cost", width: 140 },
  { field: "fertilizers_cost", headerName: "Fertilizers Cost", width: 150 },
];

const NurseryActivityList = ({ cropId }) => {
  const [editData, setEditData] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSuccess = () => {
    setEditData(null);
    setRefreshKey((k) => k + 1);
  };

  const columns = [
    ...baseColumns,
    {
      field: "actions",
      headerName: "Actions",
      width: 150,
      renderCell: (params) => (
        <div>
          <button
            onClick={() => setEditData(params.row)}
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
      {editData && (
        <NurseryActivityForm
          cropId={cropId}
          editData={editData}
          onSuccess={handleSuccess}
        />
      )}

      <CropList
        key={refreshKey}
        title="Nursery Activities"
        endpoint={`/api/crop-management/activities/nursery-activities/?crop_id=${cropId}`}
        columns={columns}
      />
    </div>
  );
};

export default NurseryActivityList;

