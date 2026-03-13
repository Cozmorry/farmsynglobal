// src/components/Layout/ProtectedRoute.jsx
import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { UsersContext } from "../../context/UsersContext";

export default function ProtectedRoute({ children }) {
  const { user } = useContext(UsersContext);

  if (!user) return <Navigate to="/login" replace />;

  return children;
}
