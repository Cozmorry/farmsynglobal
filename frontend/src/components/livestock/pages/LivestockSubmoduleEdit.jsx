// src/pages/livestock/LivestockSubmoduleEdit.jsx
import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import LivestockSubmoduleForm from "../forms/LivestockSubmoduleForm";
import { Container, Typography, CircularProgress, Alert } from "@mui/material";
import * as api from "../api/LivestockApi";

export default function LivestockSubmoduleEdit() {
  const { submodule, id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await api[submodule].get(id);
        setData(res.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load record.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [submodule, id]);

  const handleSuccess = () => {
    navigate(`/livestock/${submodule}`);
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Edit {submodule.charAt(0).toUpperCase() + submodule.slice(1)}
      </Typography>

      <LivestockSubmoduleForm
        submodule={submodule}
        editData={data}
        onSuccess={handleSuccess}
      />
    </Container>
  );
}
