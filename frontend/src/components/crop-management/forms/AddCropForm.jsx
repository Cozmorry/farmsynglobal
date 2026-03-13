//src/components/crop-management/forms/AddCropForm.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const AddCropForm = () => {
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: call API to create a crop
    console.log("Creating crop:", name);
    navigate("/crop-management/dashboard");
  };

  return (
    <div>
      <h2>Add New Crop</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Crop Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <button type="submit">Add Crop</button>
      </form>
    </div>
  );
};

export default AddCropForm;
