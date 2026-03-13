// src/components/veterinary/VeterinaryFileUpload.jsx
import React, { useEffect, useState } from "react";
import {
  uploadVeterinaryRecommendationFile,
  getVeterinaryRecommendationUploads,
  uploadVeterinaryHealthFile,
  getVeterinaryHealthUploads,
} from "./api/veterinaryApi";

const VeterinaryFileUpload = ({ type = "recommendation", id }) => {
  if (!id) return null;

  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");
  const [uploads, setUploads] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchUploads = async () => {
    try {
      const res =
        type === "recommendation"
          ? await getVeterinaryRecommendationUploads({ recommendation_id: id })
          : await getVeterinaryHealthUploads({ health_id: id });

      setUploads(res.data || []);
    } catch (err) {
      console.error("Error fetching uploads", err);
    }
  };

  useEffect(() => {
    fetchUploads();
  }, [id, type]);

  const handleUpload = async () => {
    if (!file) return alert("Select a file first");

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append(
        type === "recommendation" ? "recommendation_id" : "health_id",
        id
      );
      formData.append("file", file);
      if (description) formData.append("description", description);

      type === "recommendation"
        ? await uploadVeterinaryRecommendationFile(formData)
        : await uploadVeterinaryHealthFile(formData);

      setFile(null);
      setDescription("");
      fetchUploads();
    } catch (err) {
      console.error("Upload failed", err);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "1rem" }}>
      <h4>Veterinary {type} Files</h4>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <input
        type="text"
        placeholder="Optional description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>

      <ul>
        {uploads.map((u) => (
          <li key={u.id}>
            <a href={u.file_path} target="_blank" rel="noopener noreferrer">
              {u.file_path.split("/").pop()}
            </a>
            {u.description && ` – ${u.description}`}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VeterinaryFileUpload;

