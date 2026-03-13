// src/components/agronomy/AgronomyFileUpload.jsx
import React, { useState, useEffect } from "react";
import {
  uploadRecommendationFile,
  getRecommendationUploads,
  deleteRecommendationFile,
  uploadObservationFile,
  getObservationUploads,
  deleteObservationFile,
} from "./api/agronomyApi";

const AgronomyFileUpload = ({ type = "recommendation", id }) => {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");
  const [uploads, setUploads] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch uploaded files
  const fetchUploads = async () => {
    try {
      if (type === "recommendation") {
        const res = await getRecommendationUploads({ recommendation_id: id });
        setUploads(res.data);
      } else {
        const res = await getObservationUploads({ observation_id: id });
        setUploads(res.data);
      }
    } catch (err) {
      console.error("Error fetching uploads:", err);
    }
  };

  useEffect(() => {
    fetchUploads();
  }, [id, type]);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first!");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append(type === "recommendation" ? "recommendation_id" : "observation_id", id);
      formData.append("file", file);
      if (description) formData.append("description", description);

      if (type === "recommendation") {
        await uploadRecommendationFile(formData);
      } else {
        await uploadObservationFile(formData);
      }

      setFile(null);
      setDescription("");
      fetchUploads();
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed, check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (fileId) => {
    if (!window.confirm("Are you sure you want to delete this file?")) return;
    try {
      if (type === "recommendation") {
        await deleteRecommendationFile(fileId);
      } else {
        await deleteObservationFile(fileId);
      }
      fetchUploads();
    } catch (err) {
      console.error("Delete failed:", err);
      alert("Delete failed, check console for details.");
    }
  };

  return (
    <div style={{ marginTop: "1rem", padding: "0.5rem", border: "1px solid #ccc" }}>
      <h4>{type === "recommendation" ? "Recommendation" : "Observation"} Uploads</h4>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "0.5rem" }}>
        <input type="file" onChange={handleFileChange} />
        <input
          type="text"
          placeholder="Optional description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Uploading..." : "Upload File"}
        </button>
      </div>

      {uploads.length === 0 ? (
        <p>No files uploaded yet.</p>
      ) : (
        <ul>
          {uploads.map((u) => (
            <li key={u.id} style={{ marginBottom: "0.25rem" }}>
              <a href={u.file_path} target="_blank" rel="noopener noreferrer">
                {u.file_path.split("/").pop()}
              </a>
              {u.description && ` - ${u.description}`}
              {u.created_at && ` (Uploaded: ${new Date(u.created_at).toLocaleDateString()})`}
              <button
                style={{ marginLeft: "0.5rem", color: "red" }}
                onClick={() => handleDelete(u.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AgronomyFileUpload;
