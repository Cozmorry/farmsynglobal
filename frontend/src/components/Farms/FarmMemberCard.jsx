//src/components/Farms/FarmMemberCard.jsx
export default function FarmMemberCard({ member, onRemove }) {
  return (
    <div style={{ border: "1px solid #ccc", padding: 10, marginBottom: 5 }}>
      <strong>{member.user.username || member.user.email}</strong> - {member.role}
      {onRemove && (
        <button
          style={{ marginLeft: 10, color: "red" }}
          onClick={() => onRemove(member.id)}
        >
          Remove
        </button>
      )}
    </div>
  );
}
