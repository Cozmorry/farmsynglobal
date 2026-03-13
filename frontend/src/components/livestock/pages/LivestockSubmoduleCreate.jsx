// src/pages/livestock/LivestockSubmoduleCreate.jsx
import { useNavigate, useParams } from "react-router-dom";
import LivestockSubmoduleForm from "../forms/LivestockSubmoduleForm";
import { Container, Typography } from "@mui/material";

export default function LivestockSubmoduleCreate() {
  const { submodule } = useParams();
  const navigate = useNavigate();

  const handleSuccess = () => {
    // Navigate back to the list page after creating
    navigate(`/livestock/${submodule}`);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Create New {submodule.charAt(0).toUpperCase() + submodule.slice(1)}
      </Typography>

      <LivestockSubmoduleForm submodule={submodule} onSuccess={handleSuccess} />
    </Container>
  );
}
