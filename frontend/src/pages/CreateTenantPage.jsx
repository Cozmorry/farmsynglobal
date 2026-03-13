// src/pages/CreateTenantPage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function CreateTenantPage() {
  const navigate = useNavigate();

  const [tenantData, setTenantData] = useState({
    name: "",
    email: "",
    address: "",
    phoneNumber: "",
    selectedModules: [],
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Step to collect basic tenant details (name, email, etc.)
  const handleChange = (e) => {
    const { name, value } = e.target;
    setTenantData((prev) => ({ ...prev, [name]: value }));
  };

  const toggleModule = (module) => {
    if (tenantData.selectedModules.includes(module)) {
      setTenantData({
        ...tenantData,
        selectedModules: tenantData.selectedModules.filter((m) => m !== module),
      });
    } else {
      setTenantData({
        ...tenantData,
        selectedModules: [...tenantData.selectedModules, module],
      });
    }
  };

  const handleCreateTenant = async (e) => {
    e.preventDefault();
    setError("");

    if (tenantData.selectedModules.length === 0) {
      setError("Select at least one module");
      return;
    }

    try {
      setLoading(true);
      const res = await api.post("/tenants", tenantData); // API POST to create tenant
      setLoading(false);

      // Navigate to the tenant's dashboard or details page
      navigate(`/tenants/${res.data.id}/dashboard`);
    } catch (err) {
      setLoading(false);
      setError("Failed to create tenant");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto" }}>
      <h1>Create New Tenant</h1>
      <form onSubmit={handleCreateTenant}>
        {error && <p style={{ color: "red" }}>{error}</p>}
        
        {/* Tenant Basic Info */}
        <input
          type="text"
          name="name"
          placeholder="Tenant Name"
          value={tenantData.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Tenant Email"
          value={tenantData.email}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="address"
          placeholder="Tenant Address"
          value={tenantData.address}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="phoneNumber"
          placeholder="Tenant Phone Number"
          value={tenantData.phoneNumber}
          onChange={handleChange}
        />

        {/* Modules Selection */}
        <h3>Select Modules</h3>
        {["crop", "livestock", "poultry", "aquaculture"].map((module) => (
          <div key={module}>
            <input
              type="checkbox"
              checked={tenantData.selectedModules.includes(module)}
              onChange={() => toggleModule(module)}
            />
            <label>{module}</label>
          </div>
        ))}

        <button type="submit" disabled={loading}>
          {loading ? "Creating..." : "Create Tenant"}
        </button>
      </form>
    </div>
  );
}
