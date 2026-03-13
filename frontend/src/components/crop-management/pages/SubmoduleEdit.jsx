//src/components/crop-management/pages/SubmoduleEdit.jsx
import { useParams, useNavigate } from "react-router-dom";
import SubmoduleForm from "../forms/SubmoduleForm";

export default function SubmoduleEdit() {
  const { cropId, submodule, activityId } = useParams();
  const navigate = useNavigate();

  return (
    <SubmoduleForm
      submodule={submodule}
      cropId={Number(cropId)}
      editData={{ id: Number(activityId) }} // fetch if needed
      onSuccess={() => navigate(-1)}
    />
  );
}
