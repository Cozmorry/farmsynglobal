import React, { useEffect, useState } from "react";
import { getActivities, deleteActivity } from "../api/aquacultureApi";
import { Link } from "react-router-dom";

export default function ActivityList({ pondId }) {
  const [activities, setActivities] = useState([]);

  const fetchData = async () => {
    try {
      const res = await getActivities({ pond_id: pondId });
      const activitiesArray = Array.isArray(res.data) ? res.data : res.data?.activities || [];
      setActivities(activitiesArray);
    } catch (err) {
      console.error("Failed to fetch activities:", err);
      setActivities([]);
    }
  };

  useEffect(() => {
    if (pondId) fetchData();
  }, [pondId]);

  const handleDelete = async (id) => {
    if (window.confirm("Delete this activity?")) {
      await deleteActivity(id);
      fetchData();
    }
  };

  return (
    <div>
      <h3>Activities</h3>
      <Link to={`/aquaculture/activity/new?pond_id=${pondId}`}>
        <button>Add New Activity</button>
      </Link>
      <ul>
        {activities.length > 0 ? (
          activities.map((a) => (
            <li key={a.id}>
              {a.date} — {a.activity_type} — {a.description || "No description"} — Cost: {a.cost}
              <button onClick={() => handleDelete(a.id)} style={{ marginLeft: 10 }}>
                Delete
              </button>
            </li>
          ))
        ) : (
          <li>No activities found</li>
        )}
      </ul>
    </div>
  );
}
