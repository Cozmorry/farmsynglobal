// src/components/veterinary/api/veterinaryHealthApi.js
import axios from "axios";

// ============================
// Health Records
// ============================
export const getVeterinaryHealthRecords = async (animalGroupId, groupType) => {
  const res = await axios.get(
    `/api/veterinary/health-records?animal_group_id=${animalGroupId}&group_type=${groupType}`
  );
  return res.data;
};

export const createVeterinaryHealthRecord = async (animalGroupId, groupType, data) => {
  const res = await axios.post("/api/veterinary/health-records", {
    animal_group_id: animalGroupId,
    group_type: groupType,
    ...data,
  });
  return res.data;
};

export const updateVeterinaryHealthRecord = async (id, groupType, data) => {
  const res = await axios.put(`/api/veterinary/health-records/${id}`, {
    group_type: groupType,
    ...data,
  });
  return res.data;
};

export const deleteVeterinaryHealthRecord = async (id, groupType) => {
  const res = await axios.delete(`/api/veterinary/health-records/${id}`, {
    data: { group_type: groupType }, // some APIs expect DELETE payload
  });
  return res.data;
};
