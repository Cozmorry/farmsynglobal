//src/components/crop_management/pages/SafeTestDashboard.jsx
import React, { useEffect, useState } from "react";
import {
  getCropActivities,
  getChemicalApplications,
  getCropRotations,
  getFertilizerApplications,
  getLandPreparations,
  getNurseryActivities,
  getScoutingActivities,
  getSoilAmendments,
  getSoilTests,
  getWeedingActivities,
} from "./api/cropManagement"; // adjust path as needed

const SafeTestDashboard = () => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    const cropId = 1; // test with crop ID 1
    const fetchData = async () => {
      setLoading(true);
      const tempData = {};
      const tempErrors = [];

      const endpoints = [
        { name: "Crop Activities", fn: () => getCropActivities(cropId) },
        { name: "Chemical Applications", fn: () => getChemicalApplications(cropId) },
        { name: "Crop Rotations", fn: () => getCropRotations(cropId) },
        { name: "Fertilizer Applications", fn: () => getFertilizerApplications(cropId) },
        { name: "Land Preparations", fn: () => getLandPreparations(cropId) },
        { name: "Nursery Activities", fn: () => getNurseryActivities(cropId) },
        { name: "Scouting Activities", fn: () => getScoutingActivities(cropId) },
        { name: "Soil Amendments", fn: () => getSoilAmendments(cropId) },
        { name: "Soil Tests", fn: () => getSoilTests(cropId) },
        { name: "Weeding Activities", fn: () => getWeedingActivities(cropId) },
      ];

      for (const ep of endpoints) {
        try {
          const res = await ep.fn();
          tempData[ep.name] = res.data;
        } catch (err) {
          tempErrors.push(`${ep.name}: ${err.message}`);
        }
      }

      setData(tempData);
      setErrors(tempErrors);
      setLoading(false);
    };

    fetchData();
  }, []);

  if (loading) return <p>Loading data...</p>;

  return (
    <div>
      <h1>Safe Test Dashboard</h1>

      {errors.length > 0 && (
        <div style={{ color: "red" }}>
          <h3>Errors:</h3>
          <ul>
            {errors.map((e, i) => (
              <li key={i}>{e}</li>
            ))}
          </ul>
        </div>
      )}

      {Object.keys(data).map((key) => (
        <div key={key}>
          <h2>{key}</h2>
          <pre>{JSON.stringify(data[key], null, 2)}</pre>
        </div>
      ))}
    </div>
  );
};

export default SafeTestDashboard;
