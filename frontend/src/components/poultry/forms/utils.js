// src/components/poultry/forms/utils.js

// Convert backend date → yyyy-mm-dd for input[type="date"]
export const normalizeDate = (date) => {
  if (!date) return "";
  return new Date(date).toISOString().split("T")[0];
};

// Convert empty strings → null, strings → numbers
export const number = (value) => {
  if (value === "" || value === null || value === undefined) return null;
  return Number(value);
};
