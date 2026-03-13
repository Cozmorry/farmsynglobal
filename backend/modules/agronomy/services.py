# backend/modules/agronomy/services.py
from sqlalchemy.orm import Session
from . import models
from typing import List, Optional

# ============================================================
# Recommendations
# ============================================================

def create_recommendation(db: Session, rec_data: dict) -> models.AgronomyRecommendation:
    """Create a new recommendation."""
    rec = models.AgronomyRecommendation(**rec_data)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def list_agronomy_recommendations(
    db: Session,
    block_id: Optional[int] = None,
    crop_id: Optional[int] = None
) -> List[models.AgronomyRecommendation]:
    """List recommendations optionally filtered by block or crop."""
    query = db.query(models.AgronomyRecommendation)
    if block_id:
        query = query.filter(models.AgronomyRecommendation.block_id == block_id)
    if crop_id:
        query = query.filter(models.AgronomyRecommendation.crop_id == crop_id)
    return query.all()

# ------------------------------------------------------------
# Recommendation Uploads
# ------------------------------------------------------------

def upload_recommendation_file(
    db: Session,
    recommendation_id: int,
    file_path: str,
    file_type: str,
    description: Optional[str] = None
) -> models.AgronomyUpload:
    """Store a file upload for a recommendation."""
    upload = models.AgronomyUpload(
        recommendation_id=recommendation_id,
        file_path=file_path,
        file_type=file_type,
        description=description
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload

def get_recommendation_uploads(
    db: Session,
    recommendation_id: Optional[int] = None
) -> List[models.AgronomyUpload]:
    """Retrieve uploaded files for recommendations."""
    query = db.query(models.AgronomyUpload)
    if recommendation_id:
        query = query.filter(models.AgronomyUpload.recommendation_id == recommendation_id)
    return query.all()


# ============================================================
# Observations
# ============================================================

def create_observation(db: Session, obs_data: dict) -> models.AgronomyObservation:
    """Create a new observation."""
    obs = models.AgronomyObservation(**obs_data)
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs

def list_observations(
    db: Session,
    crop_id: Optional[int] = None,
    block_id: Optional[int] = None
) -> List[models.AgronomyObservation]:
    """List observations, optionally filtered by crop or block."""
    query = db.query(models.AgronomyObservation)
    if crop_id:
        query = query.filter(models.AgronomyObservation.crop_id == crop_id)
    if block_id:
        query = query.filter(models.AgronomyObservation.block_id == block_id)
    return query.all()


# ------------------------------------------------------------
# Observation Uploads
# ------------------------------------------------------------

def upload_observation_file(
    db: Session,
    observation_id: int,
    file_path: str,
    file_type: str,
    description: Optional[str] = None
) -> models.AgronomyObservationUpload:
    """Store a file upload for an observation."""
    upload = models.AgronomyObservationUpload(
        observation_id=observation_id,
        file_path=file_path,
        file_type=file_type,
        description=description
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload

def get_observation_uploads(
    db: Session,
    observation_id: Optional[int] = None
) -> List[models.AgronomyObservationUpload]:
    """Retrieve uploaded files for observations."""
    query = db.query(models.AgronomyObservationUpload)
    if observation_id:
        query = query.filter(models.AgronomyObservationUpload.observation_id == observation_id)
    return query.all()


# ============================================================
# Recommendation Generation (example)
# ============================================================

from backend.modules.crop_management.models import Crop, Scouting, FertilizerApplication

def generate_agronomy_recommendations(db: Session, crop_id: int) -> List[models.AgronomyRecommendation]:
    """Generate recommendations based on crop activities."""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        return []

    recommendations = []

    # Example: Scouting
    for scout in crop.scouting_records:
        if scout.pests:
            recommendations.append({
                "farm_id": crop.farm_id,
                "crop_id": crop.id,
                "block_id": crop.block_id,
                "recommendation_text": f"Observed pests: {scout.pests}. Consider treatment.",
                "recommended_action": "Spray chemical",
                "generated_by": "system",
                "source": "scouting"
            })

    # Example: Fertilizer (simple check)
    for fert in crop.fertilizer_applications:
        recommended_qty = getattr(fert, "recommended_quantity_kg", 0)
        if getattr(fert, "quantity_kg", 0) < recommended_qty:
            recommendations.append({
                "farm_id": crop.farm_id,
                "crop_id": crop.id,
                "block_id": crop.block_id,
                "recommendation_text": f"Fertilizer {getattr(fert, 'fertilizer_name', 'N/A')} below recommended rate.",
                "recommended_action": "Apply additional fertilizer",
                "generated_by": "system",
                "source": "fertilizer_report"
            })

    rec_objects = [create_recommendation(db, rec) for rec in recommendations]
    return rec_objects

