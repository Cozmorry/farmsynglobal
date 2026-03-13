// src/components/veterinary/VeterinaryRecommendations.jsx
import React, { useEffect, useState } from "react";
import {
  getVeterinaryRecommendations,
  createVeterinaryRecommendation,
  updateVeterinaryRecommendation,
  deleteVeterinaryRecommendation,
} from "./api/veterinaryApi";

import {
  Box,
  Button,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  IconButton,
  Typography,
  CircularProgress,
} from "@mui/material";
import { Delete, Edit, Save, Cancel } from "@mui/icons-material";

const VeterinaryRecommendations = () => {
  // ============================
  // STATE
  // ============================
  const [recommendations, setRecommendations] = useState([]); // MUST be []
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    recommendation_text: "",
    recommended_action: "",
    animal_group_id: "",
  });

  const [editId, setEditId] = useState(null);
  const [editData, setEditData] = useState({
    recommendation_text: "",
    recommended_action: "",
  });

  // ============================
  // FETCH
  // ============================
  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const res = await getVeterinaryRecommendations();

      // Defensive: backend may return { data: [...] } OR [...]
      const data = Array.isArray(res?.data)
        ? res.data
        : Array.isArray(res?.data?.data)
        ? res.data.data
        : [];

      setRecommendations(data);
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  // ============================
  // HANDLERS
  // ============================
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createVeterinaryRecommendation(formData);
      setFormData({
        recommendation_text: "",
        recommended_action: "",
        animal_group_id: "",
      });
      fetchRecommendations();
    } catch (error) {
      console.error("Failed to create recommendation:", error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteVeterinaryRecommendation(id);
      fetchRecommendations();
    } catch (error) {
      console.error("Failed to delete recommendation:", error);
    }
  };

  const startEdit = (rec) => {
    setEditId(rec.id);
    setEditData({
      recommendation_text: rec.recommendation_text || "",
      recommended_action: rec.recommended_action || "",
    });
  };

  const cancelEdit = () => {
    setEditId(null);
    setEditData({
      recommendation_text: "",
      recommended_action: "",
    });
  };

  const saveEdit = async () => {
    try {
      await updateVeterinaryRecommendation(editId, editData);
      cancelEdit();
      fetchRecommendations();
    } catch (error) {
      console.error("Failed to update recommendation:", error);
    }
  };

  // ============================
  // UI
  // ============================
  return (
    <Box p={3}>
      <Typography variant="h5" gutterBottom>
        Veterinary Recommendations
      </Typography>

      {/* CREATE */}
      <Box
        component="form"
        onSubmit={handleSubmit}
        mb={3}
        display="flex"
        gap={2}
        flexWrap="wrap"
      >
        <TextField
          label="Recommendation Text"
          name="recommendation_text"
          value={formData.recommendation_text}
          onChange={handleChange}
          required
          fullWidth
        />
        <TextField
          label="Recommended Action"
          name="recommended_action"
          value={formData.recommended_action}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Animal Group ID"
          name="animal_group_id"
          type="number"
          value={formData.animal_group_id}
          onChange={handleChange}
        />
        <Button type="submit" variant="contained">
          Add
        </Button>
      </Box>

      {/* LOADING */}
      {loading && (
        <Box display="flex" justifyContent="center" my={3}>
          <CircularProgress />
        </Box>
      )}

      {/* EMPTY STATE */}
      {!loading && recommendations.length === 0 && (
        <Typography>No veterinary recommendations found.</Typography>
      )}

      {/* LIST */}
      {!loading && recommendations.length > 0 && (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Recommendation</TableCell>
              <TableCell>Action</TableCell>
              <TableCell>Animal Group</TableCell>
              <TableCell>Operations</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {recommendations.map((rec) => (
              <TableRow key={rec.id}>
                <TableCell>{rec.id}</TableCell>

                <TableCell>
                  {editId === rec.id ? (
                    <TextField
                      name="recommendation_text"
                      value={editData.recommendation_text}
                      onChange={handleEditChange}
                      fullWidth
                    />
                  ) : (
                    rec.recommendation_text
                  )}
                </TableCell>

                <TableCell>
                  {editId === rec.id ? (
                    <TextField
                      name="recommended_action"
                      value={editData.recommended_action}
                      onChange={handleEditChange}
                      fullWidth
                    />
                  ) : (
                    rec.recommended_action
                  )}
                </TableCell>

                <TableCell>{rec.animal_group_id}</TableCell>

                <TableCell>
                  {editId === rec.id ? (
                    <>
                      <IconButton onClick={saveEdit} color="primary">
                        <Save />
                      </IconButton>
                      <IconButton onClick={cancelEdit} color="secondary">
                        <Cancel />
                      </IconButton>
                    </>
                  ) : (
                    <>
                      <IconButton onClick={() => startEdit(rec)}>
                        <Edit />
                      </IconButton>
                      <IconButton
                        onClick={() => handleDelete(rec.id)}
                        color="error"
                      >
                        <Delete />
                      </IconButton>
                    </>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </Box>
  );
};

export default VeterinaryRecommendations;
