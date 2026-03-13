// src/components/pages/CropUploadList.jsx
import React from "react";
import CropList from "./CropList";

const columns = [
  { field: "id", headerName: "ID", width: 70 },
  { field: "activity_type", headerName: "Activity Type", width: 150 },
  { field: "activity_id", headerName: "Activity ID", width: 120 },
  { field: "file_type", headerName: "File Type", width: 120 },
  { field: "description", headerName: "Description", width: 180 },
  { field: "file_url", headerName: "File URL", width: 200,
    renderCell: (params) => (
      <a href={params.value} target="_blank" rel="noopener noreferrer">
        View
      </a>
    )
  },
  { field: "uploaded_at", headerName: "Uploaded At", width: 150,
    valueFormatter: (params) => params.value ? new Date(params.value).toLocaleString() : "-"
  },
  {
    field: "actions",
    headerName: "Actions",
    width: 150,
    renderCell: (params) => (
      <div>
        <button onClick={() => console.log("Delete", params.row.id)} style={{ color: "red" }}>
          Delete
        </button>
      </div>
    ),
  },
];

const CropUploadList = () => (
  <CropList
    title="Crop Activity Uploads"
    endpoint="/crop_management/activity_uploads"
    columns={columns}
  />
);

export default CropUploadList;

