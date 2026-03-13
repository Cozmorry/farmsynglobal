//src/components/aquaculture/AquacultureRoutes.jsx
import React from "react";
import { Routes, Route, Navigate, useParams } from "react-router-dom";

/* Dashboard */
import AquacultureDashboard from "./pages/AquacultureDashboard";

/* Lists (pages) */
import PondList from "./pages/PondList";
import WaterQualityList from "./pages/WaterQualityList";
import ActivityList from "./pages/ActivityList";
import FeedingList from "./pages/FeedingList";
import ProductionList from "./pages/ProductionList";
import HarvestList from "./pages/HarvestList";
import HealthList from "./pages/HealthList";
import RecommendationList from "./pages/RecommendationList";

/* Forms */
import NewPond from "./forms/NewPond";
import NewWaterQuality from "./forms/NewWaterQuality";
import NewActivity from "./forms/NewActivity";
import NewFeeding from "./forms/NewFeeding";
import NewProduction from "./forms/NewProduction";
import NewHarvest from "./forms/NewHarvest";
import NewHealth from "./forms/NewHealth";
import NewRecommendation from "./forms/NewRecommendation";

export default function AquacultureRoutes() {
  return (
    <Routes>
      {/* Dashboard */}
      <Route index element={<AquacultureDashboard />} />

      {/* Redirect /aquaculture -> dashboard */}
      <Route path="/" element={<Navigate to="" replace />} />

      {/* Ponds */}
      <Route path="ponds" element={<PondList />} />
      <Route path="ponds/new" element={<NewPond />} />

      {/* Water Quality */}
      <Route path="ponds/:pondId/water_quality" element={<WaterQualityWrapper />} />
      <Route path="water_quality/new" element={<NewWaterQuality />} />

      {/* Activities */}
      <Route path="ponds/:pondId/activity" element={<ActivityWrapper />} />
      <Route path="activity/new" element={<NewActivity />} />

      {/* Feeding */}
      <Route path="ponds/:pondId/feedings" element={<FeedingWrapper />} />
      <Route path="feedings/new" element={<NewFeeding />} />

      {/* Production */}
      <Route path="ponds/:pondId/production" element={<ProductionWrapper />} />
      <Route path="production/new" element={<NewProduction />} />

      {/* Harvest */}
      <Route path="ponds/:pondId/harvest" element={<HarvestWrapper />} />
      <Route path="harvest/new" element={<NewHarvest />} />

      {/* Health */}
      <Route path="ponds/:pondId/health" element={<HealthWrapper />} />
      <Route path="health/new" element={<NewHealth />} />

      {/* Recommendations */}
      <Route
        path="health/:healthId/recommendations"
        element={<RecommendationWrapper />}
      />
      <Route path="recommendation/new" element={<NewRecommendation />} />
    </Routes>
  );
}

/* ===================== */
/* Param Wrappers        */
/* ===================== */

function WaterQualityWrapper() {
  const { pondId } = useParams();
  return <WaterQualityList pondId={pondId} />;
}

function ActivityWrapper() {
  const { pondId } = useParams();
  return <ActivityList pondId={pondId} />;
}

function FeedingWrapper() {
  const { pondId } = useParams();
  return <FeedingList pondId={pondId} />;
}

function ProductionWrapper() {
  const { pondId } = useParams();
  return <ProductionList pondId={pondId} />;
}

function HarvestWrapper() {
  const { pondId } = useParams();
  return <HarvestList pondId={pondId} />;
}

function HealthWrapper() {
  const { pondId } = useParams();
  return <HealthList pondId={pondId} />;
}

function RecommendationWrapper() {
  const { healthId } = useParams();
  return <RecommendationList healthId={healthId} />;
}

<Route
  path="ponds/:pondId"
  element={<AquacultureDashboard />}
/>
