//src/components/agronomy/AgronomyDashboard.jsx
import React, { useState } from "react";
import { Box, Tabs, Tab, Typography } from "@mui/material";
import AgronomyRecommendations from "./AgronomyRecommendations";
import AgronomyObservations from "./AgronomyObservations";

const AgronomyDashboard = ({ cropId, blockId }) => {
  const [tabIndex, setTabIndex] = useState(0);

  const handleChange = (event, newValue) => {
    setTabIndex(newValue);
  };

  return (
    <Box p={3}>
      <Typography variant="h3" mb={3}>Agronomy Dashboard</Typography>

      <Tabs value={tabIndex} onChange={handleChange} sx={{ mb: 2 }}>
        <Tab label="Recommendations" />
        <Tab label="Observations" />
      </Tabs>

      <Box>
        {tabIndex === 0 && <AgronomyRecommendations cropId={cropId} blockId={blockId} />}
        {tabIndex === 1 && <AgronomyObservations cropId={cropId} blockId={blockId} />}
      </Box>
    </Box>
  );
};

export default AgronomyDashboard;
