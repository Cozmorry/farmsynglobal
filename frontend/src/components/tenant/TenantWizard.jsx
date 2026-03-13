// src/components/tenant/TenantWizard.jsx
import React, { useState } from "react";
import { createTenant, assignModules } from "../../api/tenants";

export default function TenantWizard() {
  const [step, setStep] = useState(1);
  const [tenant, setTenant] = useState({
    name: "",
    email: "",
    address: "",
    phone_number: "",
    selected_modules: [],
  });

  const MODULES = [
    "crop",
    "agronomy",
    "livestock",
    "veterinary",
    "poultry",
    "aquaculture",
    "finance",
    "store_inventory",
    "hr",
  ];

  const handleNext = async () => {
    try {
      if (step === 1) {
        // Step 1: create tenant
        const res = await createTenant({
          name: tenant.name,
          email: tenant.email,
          address: tenant.address,
          phone_number: tenant.phone_number,
          selected_modules: [],
        });
        setTenant(res);
        setStep(2);
      } else if (step === 2) {
        // Step 2: assign modules
        const res = await assignModules(tenant.id, tenant.selected_modules);
        setTenant(res);
        setStep(3);
      }
    } catch (err) {
      console.error(err);
      alert("Failed to proceed. Check console for details.");
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px" }}>
      <h2>Tenant Onboarding</h2>

      {step === 1 && (
        <div>
          <input placeholder="Name" value={tenant.name} onChange={e => setTenant({...tenant, name: e.target.value})} />
          <input placeholder="Email" value={tenant.email} onChange={e => setTenant({...tenant, email: e.target.value})} />
          <input placeholder="Address" value={tenant.address} onChange={e => setTenant({...tenant, address: e.target.value})} />
          <input placeholder="Phone" value={tenant.phone_number} onChange={e => setTenant({...tenant, phone_number: e.target.value})} />
        </div>
      )}

      {step === 2 && (
        <div>
          <h3>Select Modules</h3>
          {MODULES.map(mod => (
            <div key={mod}>
              <input
                type="checkbox"
                checked={tenant.selected_modules.includes(mod)}
                onChange={e => {
                  const modules = e.target.checked
                    ? [...tenant.selected_modules, mod]
                    : tenant.selected_modules.filter(m => m !== mod);
                  setTenant({ ...tenant, selected_modules: modules });
                }}
              />
              {mod.replace("_", " ").toUpperCase()}
            </div>
          ))}
        </div>
      )}

      {step === 3 && (
        <div>
          <h3>Success!</h3>
          <p>Tenant <strong>{tenant.name}</strong> created with modules:</p>
          <ul>
            {tenant.selected_modules.map(m => <li key={m}>{m}</li>)}
          </ul>
        </div>
      )}

      {step < 3 && <button onClick={handleNext}>Next</button>}
    </div>
  );
}
