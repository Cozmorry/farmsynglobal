# backend/modules/agronomy/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# ============================================================
# Recommendation Schemas
# ============================================================

class AgronomyRecommendationBase(BaseModel):
    recommendation_text: str
    recommended_action: Optional[str]
    source: Optional[str]


class AgronomyRecommendationCreate(AgronomyRecommendationBase):
    farm_id: int
    block_id: Optional[int]
    crop_id: int
    generated_by: Optional[str]


class AgronomyRecommendationRead(AgronomyRecommendationBase):
    id: int
    farm_id: int
    block_id: Optional[int]
    crop_id: int
    date_given: date
    generated_by: Optional[str]

    class Config:
        from_attributes = True


# ============================================================
# Recommendation Upload Schemas
# ============================================================

class AgronomyRecommendationUploadBase(BaseModel):
    file_type: Optional[str]
    description: Optional[str]


class AgronomyRecommendationUploadCreate(AgronomyRecommendationUploadBase):
    recommendation_id: int
    file_path: str


class AgronomyRecommendationUploadRead(AgronomyRecommendationUploadBase):
    id: int
    recommendation_id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# Observation Schemas
# ============================================================

class AgronomyObservationBase(BaseModel):
    notes: str
    pest_issues: Optional[str]
    disease_issues: Optional[str]
    nutrient_deficiencies: Optional[str]
    suggested_action: Optional[str]
    reported_by: Optional[str]


class AgronomyObservationCreate(AgronomyObservationBase):
    crop_id: int
    block_id: Optional[int]
    observation_date: Optional[date] = None


class AgronomyObservationRead(AgronomyObservationBase):
    id: int
    crop_id: int
    block_id: Optional[int]
    observation_date: date

    class Config:
        from_attributes = True


# ============================================================
# Observation Upload Schemas
# ============================================================

class AgronomyObservationUploadBase(BaseModel):
    file_type: Optional[str]
    description: Optional[str]


class AgronomyObservationUploadCreate(AgronomyObservationUploadBase):
    observation_id: int
    file_path: str


class AgronomyObservationUploadRead(AgronomyObservationUploadBase):
    id: int
    observation_id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

