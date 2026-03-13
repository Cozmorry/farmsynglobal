// src/components/crop_management/CropManagementRoutes.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

/* ======================
   DASHBOARD & DETAIL
====================== */
import CropDashboard from "./pages/CropDashboard";
import CropDetailDashboard from "./pages/CropDetailDashboard";
import AddCropForm from "./forms/AddCropForm";
import SubmoduleCreate from "./pages/SubmoduleCreate";

/* ======================
   LIST PAGES
====================== */
import CropActivityList from "./pages/CropActivityList";
import LandPreparationList from "./pages/LandPreparationList";
import NurseryActivityList from "./pages/NurseryActivityList";
import FertilizerApplicationList from "./pages/FertilizerApplicationList";
import ChemicalApplicationList from "./pages/ChemicalApplicationList";
import WeedingList from "./pages/WeedingList";
import ScoutingList from "./pages/ScoutingList";
import SoilTestList from "./pages/SoilTestList";
import SoilAmendmentList from "./pages/SoilAmendmentList";
import CropRotationList from "./pages/CropRotationList";
import CropHarvestList from "./pages/CropHarvestList";
import CropSaleList from "./pages/CropSaleList";
import CropUploadList from "./pages/CropUploadList";

/* ======================
   EDIT
====================== */
import ActivityEdit from "./pages/ActivityEdit";
import SubmoduleEdit from "./pages/SubmoduleEdit";

const CropManagementRoutes = () => {
  return (
    <Routes>
      {/* Base redirect */}
      <Route index element={<Navigate to="dashboard" replace />} />

      {/* DASHBOARD */}
      <Route path="dashboard" element={<CropDashboard />} />

      {/* CROPS */}
      <Route path="crops/new" element={<AddCropForm />} />
      <Route path="crops/:cropId" element={<CropDetailDashboard />} />

      {/* LIST PAGES (GLOBAL VIEWS) */}
      <Route path="general-activities" element={<CropActivityList />} />
      <Route path="land-preparations" element={<LandPreparationList />} />
      <Route path="nursery-activities" element={<NurseryActivityList />} />
      <Route
        path="fertilizer-applications"
        element={<FertilizerApplicationList />}
      />
      <Route
        path="chemical-applications"
        element={<ChemicalApplicationList />}
      />
      <Route path="weeding-activities" element={<WeedingList />} />
      <Route path="scouting-activities" element={<ScoutingList />} />
      <Route path="soil-tests" element={<SoilTestList />} />
      <Route path="soil-amendments" element={<SoilAmendmentList />} />
      <Route path="crop-rotations" element={<CropRotationList />} />
      <Route path="harvests" element={<CropHarvestList />} />
      <Route path="sales" element={<CropSaleList />} />
      <Route path="uploads" element={<CropUploadList />} />

      {/* CROP-SCOPED SUBMODULE FORMS */}
      <Route
        path="crops/:cropId/:submodule/new"
        element={<SubmoduleCreate />}
      />
      <Route
        path="crops/:cropId/:submodule/edit/:activityId"
        element={<SubmoduleEdit />}
      />

      {/* LEGACY / DIRECT EDIT */}
      <Route path="activity/edit/:activityId" element={<ActivityEdit />} />
    </Routes>
  );
};

{/* BLOCK CONTEXT DASHBOARD */}
<Route
  path="blocks/:blockId"
  element={<CropDashboard />}
/>

{/* GREENHOUSE CONTEXT DASHBOARD */}
<Route
  path="greenhouses/:greenhouseId"
  element={<CropDashboard />}
/>

export default CropManagementRoutes;
