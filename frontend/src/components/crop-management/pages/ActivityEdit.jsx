import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Paper,
  Typography,
  Button,
  Divider,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import axios from "axios";
import CropActivityUploadForm from "../forms/CropUpload";

const ActivityEdit = () => {
  const { activityId } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [activity, setActivity] = useState(null);
  const [uploads, setUploads] = useState([]);

  useEffect(() => {
    fetchActivity();
  }, [activityId]);

  const fetchActivity = async () => {
    try {
      const activityRes = await axios.get(
        `/crop_management/activities/general/${activityId}`
      );

      setActivity(activityRes.data);

      const uploadRes = await axios.get("/crop_management/uploads/", {
        params: {
          crop_id: activityRes.data.crop_id,
          activity_type: activityRes.data.activity_type,
        },
      });

      setUploads(
        uploadRes.data.filter(
          (u) => u.activity_id === activityRes.data.id
        )
      );
    } catch (err) {
      console.error("Failed to load activity", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Delete this activity?")) return;

    try {
      await axios.delete(
        `/crop_management/activities/general/${activityId}`
      );
      navigate(-1);
    } catch (err) {
      console.error("Delete failed", err);
    }
  };

  if (loading) {
    return (
      <center style={{ marginTop: 80 }}>
        <CircularProgress />
      </center>
    );
  }

  if (!activity) {
    return (
      <Typography color="error">
        Activity not found
      </Typography>
    );
  }

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Edit Activity
      </Typography>

      <Typography><b>Type:</b> {activity.activity_type}</Typography>
      <Typography><b>Date:</b> {activity.date}</Typography>
      <Typography><b>Description:</b> {activity.description || "-"}</Typography>

      <Divider sx={{ my: 2 }} />

      {/* ======================
         UPLOAD FORM
      ====================== */}
      <Typography variant="h6" sx={{ mb: 1 }}>
        Upload Files
      </Typography>

      <CropActivityUploadForm
        cropId={activity.crop_id}
        activityType={activity.activity_type}
        activityId={activity.id}
        onSuccess={fetchActivity}
      />

      {/* ======================
         UPLOAD LIST
      ====================== */}
      <Typography variant="h6" sx={{ mt: 3 }}>
        Uploaded Files
      </Typography>

      {uploads.length === 0 ? (
        <Typography color="text.secondary">
          No files uploaded yet.
        </Typography>
      ) : (
        <List>
          {uploads.map((u) => (
            <ListItem key={u.id}>
              <ListItemText
                primary={u.description || u.file_type}
                secondary={
                  <a
                    href={`/${u.file_path}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View / Download
                  </a>
                }
              />
            </ListItem>
          ))}
        </List>
      )}

      <Divider sx={{ my: 3 }} />

      {/* ======================
         ACTIONS
      ====================== */}
      <Button
        variant="contained"
        color="error"
        onClick={handleDelete}
      >
        Delete Activity
      </Button>
    </Paper>
  );
};

export default ActivityEdit;
