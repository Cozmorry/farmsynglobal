# backend/modules/agronomy/router.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os

from backend.core.database import get_db
from backend.modules.agronomy import schemas, services

router = APIRouter(tags=["Agronomy"])

# ============================================================
# RECOMMENDATIONS
# ============================================================

@router.post("/recommendations/", response_model=schemas.AgronomyRecommendationRead)
def create_recommendation(
    rec: schemas.AgronomyRecommendationCreate,
    db: Session = Depends(get_db)
):
    return services.create_recommendation(db, rec.dict())


@router.get("/recommendations/", response_model=List[schemas.AgronomyRecommendationRead])
def list_recommendations(
    block_id: Optional[int] = None,
    crop_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return services.list_agronomy_recommendations(db, block_id, crop_id)


@router.post("/recommendations/generate/{crop_id}", response_model=List[schemas.AgronomyRecommendationRead])
def generate_recommendations(
    crop_id: int,
    db: Session = Depends(get_db)
):
    return services.generate_agronomy_recommendations(db, crop_id)


# ----------------------------
# Recommendation Uploads
# ----------------------------

@router.post("/recommendation-uploads/", response_model=schemas.AgronomyRecommendationUploadRead)
async def upload_recommendation_file(
    recommendation_id: int = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    upload_dir = "uploads/agronomy_files"
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    saved_filename = f"rec_{recommendation_id}_{timestamp}{file_extension}"
    file_path = os.path.join(upload_dir, saved_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return services.upload_recommendation_file(
        db=db,
        recommendation_id=recommendation_id,
        file_path=file_path,
        file_type=file.content_type,
        description=description
    )


@router.get("/recommendation-uploads/", response_model=List[schemas.AgronomyRecommendationUploadRead])
def list_recommendation_uploads(
    recommendation_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return services.get_recommendation_uploads(db, recommendation_id)


# ============================================================
# OBSERVATIONS
# ============================================================

@router.post("/observations/", response_model=schemas.AgronomyObservationRead)
def create_observation(
    obs: schemas.AgronomyObservationCreate,
    db: Session = Depends(get_db)
):
    return services.create_observation(db, obs.dict())


@router.get("/observations/", response_model=List[schemas.AgronomyObservationRead])
def list_observations(
    crop_id: Optional[int] = None,
    block_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return services.list_observations(db, crop_id, block_id)


# ----------------------------
# Observation Uploads
# ----------------------------

@router.post("/observation-uploads/", response_model=schemas.AgronomyObservationUploadRead)
async def upload_observation_file(
    observation_id: int = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    upload_dir = "uploads/agronomy_observations"
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    saved_filename = f"obs_{observation_id}_{timestamp}{file_extension}"
    file_path = os.path.join(upload_dir, saved_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return services.upload_observation_file(
        db=db,
        observation_id=observation_id,
        file_path=file_path,
        file_type=file.content_type,
        description=description
    )


@router.get("/observation-uploads/", response_model=List[schemas.AgronomyObservationUploadRead])
def list_observation_uploads(
    observation_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return services.get_observation_uploads(db, observation_id)
