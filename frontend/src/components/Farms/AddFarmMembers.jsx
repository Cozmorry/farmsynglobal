// frontend/src/components/farms/AddFarmMembers.jsx
// frontend/src/components/farms/AddFarmMembers.jsx
import React, { useState, useEffect } from "react";
import api from "../../api/axios";

const ROLES = ["manager", "worker", "vet", "agronomist", "accountant"];

export default function AddFarmMembers({ farmId }) {
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState("");
  const [selectedRole, setSelectedRole] = useState(ROLES[0]);
  const [members, setMembers] = useState([]);
  const [error, setError] = useState("");

  const fetchMembers = async () => {
    try {
      const res = await api.get(`/farms/${farmId}/members`);
      setMembers(res.data);
    } catch (err) {
      console.error("Failed to load members", err);
    }
  };

  useEffect(() => {
    fetchMembers();

    const fetchUsers = async () => {
      try {
        const res = await api.get("/users"); // ensure backend supports this
        setUsers(res.data.filter(u => u.id));
      } catch (err) {
        console.error("Failed to load users", err);
      }
    };
    fetchUsers();
  }, [farmId]);

  const handleAddMember = async () => {
    if (!selectedUserId) return;

    try {
      const res = await api.post(`/farms/${farmId}/members`, {
        user_id: selectedUserId,
        role: selectedRole,
      });

      setMembers([...members, res.data]);
      setSelectedUserId("");
      setSelectedRole(ROLES[0]);
      setError("");
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Failed to add member. User may already be assigned."
      );
    }
  };

  const handleRemoveMember = async (memberId) => {
    try {
      await api.delete(`/farms/${farmId}/members/${memberId}`);
      setMembers(members.filter((m) => m.id !== memberId));
    } catch (err) {
      console.error(err);
      alert("Failed to remove member");
    }
  };

  return (
    <div className="add-farm-members">
      <h3>Manage Farm Members</h3>
      {error && <p className="error">{error}</p>}

      <div className="add-member-form">
        <select
          value={selectedUserId}
          onChange={(e) => setSelectedUserId(e.target.value)}
        >
          <option value="">-- Select User --</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.username || u.email}
            </option>
          ))}
        </select>

        <select
          value={selectedRole}
          onChange={(e) => setSelectedRole(e.target.value)}
        >
          {ROLES.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>

        <button onClick={handleAddMember}>Add Member</button>
      </div>

      <h4>Current Members</h4>
      <ul>
        {members.map((m) => (
          <li key={m.id}>
            {m.user_id} - {m.role}{" "}
            <button onClick={() => handleRemoveMember(m.id)}>Remove</button>
          </li>
        ))}
        {members.length === 0 && <p>No members yet</p>}
      </ul>
    </div>
  );
}
