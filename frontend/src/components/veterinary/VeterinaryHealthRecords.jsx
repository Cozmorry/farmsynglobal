// src/components/veterinary/VeterinaryHealthRecords.jsx
import React, { useEffect, useState } from "react";
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
  MenuItem,
} from "@mui/material";
import { Delete, Edit, Save, Cancel } from "@mui/icons-material";
import {
  getVeterinaryHealthRecords,
  createVeterinaryHealthRecord,
  updateVeterinaryHealthRecord,
  deleteVeterinaryHealthRecord,
} from "./api/veterinaryHealthApi";

const groupTypes = [
  { value: "poultry", label: "Poultry" },
  { value: "livestock", label: "Livestock" },
  { value: "aquaculture", label: "Aquaculture" },
];

const VeterinaryHealthRecords = ({ animalGroupId }) => {
  const [records, setRecords] = useState([]);
  const [formData, setFormData] = useState({
    group_type: "poultry",
    symptoms: "",
    mortality: 0,
    disease_detected: "",
    treatment_given: "",
    health_status: "",
    notes: "",
  });

  const [editId, setEditId] = useState(null);
  const [editData, setEditData] = useState({});

  const fetchRecords = async () => {
    if (!animalGroupId) return;
    const res = await getVeterinaryHealthRecords(animalGroupId, formData.group_type);
    setRecords(res.data || res); // depending on API response structure
  };

  useEffect(() => {
    fetchRecords();
  }, [animalGroupId, formData.group_type]);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });
  const handleEditChange = (e) => setEditData({ ...editData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createVeterinaryHealthRecord(animalGroupId, formData.group_type, formData);
    setFormData({
      group_type: formData.group_type,
      symptoms: "",
      mortality: 0,
      disease_detected: "",
      treatment_given: "",
      health_status: "",
      notes: "",
    });
    fetchRecords();
  };

  const handleDelete = async (id) => {
    await deleteVeterinaryHealthRecord(id, formData.group_type);
    fetchRecords();
  };

  const startEdit = (rec) => {
    setEditId(rec.id);
    setEditData({ ...rec });
  };

  const cancelEdit = () => {
    setEditId(null);
    setEditData({});
  };

  const saveEdit = async () => {
    await updateVeterinaryHealthRecord(editId, editData.group_type, editData);
    cancelEdit();
    fetchRecords();
  };

  return (
    <Box>
      <h3>Health Records</h3>

      {/* CREATE FORM */}
      <Box component="form" onSubmit={handleSubmit} display="flex" gap={2} mb={3} flexWrap="wrap">
        <TextField
          select
          label="Animal Group Type"
          name="group_type"
          value={formData.group_type}
          onChange={handleChange}
        >
          {groupTypes.map((g) => (
            <MenuItem key={g.value} value={g.value}>
              {g.label}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="Symptoms"
          name="symptoms"
          value={formData.symptoms}
          onChange={handleChange}
        />
        <TextField
          label="Mortality"
          type="number"
          name="mortality"
          value={formData.mortality}
          onChange={handleChange}
        />
        <TextField
          label="Disease Detected"
          name="disease_detected"
          value={formData.disease_detected}
          onChange={handleChange}
        />
        <TextField
          label="Treatment Given"
          name="treatment_given"
          value={formData.treatment_given}
          onChange={handleChange}
        />
        <TextField
          label="Health Status"
          name="health_status"
          value={formData.health_status}
          onChange={handleChange}
        />
        <TextField
          label="Notes"
          name="notes"
          value={formData.notes}
          onChange={handleChange}
        />

        <Button type="submit" variant="contained">Add Record</Button>
      </Box>

      {/* RECORDS TABLE */}
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Symptoms</TableCell>
            <TableCell>Mortality</TableCell>
            <TableCell>Disease</TableCell>
            <TableCell>Treatment</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Notes</TableCell>
            <TableCell>Operations</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {records.map((rec) => (
            <TableRow key={rec.id}>
              <TableCell>{rec.id}</TableCell>
              <TableCell>
                {editId === rec.id ? (
                  <TextField name="symptoms" value={editData.symptoms} onChange={handleEditChange} />
                ) : rec.symptoms}
              </TableCell>
              <TableCell>
                {editId === rec.id ? (
                  <TextField type="number" name="mortality" value={editData.mortality} onChange={handleEditChange} />
                ) : rec.mortality}
              </TableCell>
              <TableCell>
                {editId === rec.id ? (
                  <TextField name="disease_detected" value={editData.disease_detected} onChange={handleEditChange} />
                ) : rec.disease_detected}
              </TableCell>
              <TableCell>
                {editId === rec.id ? (
                  <TextField name="treatment_given" value={editData.treatment_given} onChange={handleEditChange} />
                ) : rec.treatment_given}
              </TableCell>
              <TableCell>
                {editId === rec.id ? (
                  <TextField name="health_status" value={editData.health_status} onChange={handleEditChange} />
                ) : rec.health_status}
              </TableCell>
              <TableCell>
                {editId === rec.id ? (
                  <TextField name="notes" value={editData.notes} onChange={handleEditChange} />
                ) : rec.notes}
              </TableCell>
              <TableCell>
                {editId === rec.id ? (
                  <>
                    <IconButton onClick={saveEdit}><Save /></IconButton>
                    <IconButton onClick={cancelEdit}><Cancel /></IconButton>
                  </>
                ) : (
                  <>
                    <IconButton onClick={() => startEdit(rec)}><Edit /></IconButton>
                    <IconButton onClick={() => handleDelete(rec.id)} color="error"><Delete /></IconButton>
                  </>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
};

export default VeterinaryHealthRecords;

