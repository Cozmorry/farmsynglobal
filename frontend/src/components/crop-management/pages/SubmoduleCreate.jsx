//src/components/crop-management/pages/SubmoduleCreate.jsx
import { useParams, useNavigate } from "react-router-dom";
import SubmoduleForm from "../forms/SubmoduleForm";

export default function SubmoduleCreate() {
  const { cropId, submodule } = useParams();
  const navigate = useNavigate();

  return (
    <SubmoduleForm
      submodule={submodule}
      cropId={Number(cropId)}
      onSuccess={() => navigate(-1)}
    />
  );
}
