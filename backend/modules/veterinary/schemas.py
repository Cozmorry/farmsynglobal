# backend/modules/veterinary/schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

# ============================================================
# VETERINARY RECOMMENDATION
# ============================================================
class VeterinaryRecommendationBase(BaseModel):
    recommendation_text: str
    recommended_action: Optional[str] = None
    date_given: Optional[date] = None

class VeterinaryRecommendationCreate(VeterinaryRecommendationBase):
    livestock_health_id: Optional[int] = None
    poultry_health_id: Optional[int] = None
    aquaculture_health_id: Optional[int] = None
    animal_group_id: Optional[int] = None

class VeterinaryRecommendationUpdate(BaseModel):
    recommendation_text: Optional[str] = None
    recommended_action: Optional[str] = None
    date_given: Optional[date] = None

class VeterinaryRecommendationOut(VeterinaryRecommendationBase):
    id: int
    livestock_health_id: Optional[int]
    poultry_health_id: Optional[int]
    aquaculture_health_id: Optional[int]
    animal_group_id: Optional[int]

    class Config:
        from_attributes = True


# ============================================================
# HEALTH RECORDS
# ============================================================
class HealthRecordBase(BaseModel):
    date_checked: Optional[date] = None
    symptoms: Optional[str] = None
    mortality: Optional[int] = 0
    disease_detected: Optional[str] = None
    treatment_given: Optional[str] = None
    health_status: Optional[str] = None
    notes: Optional[str] = None

class HealthRecordCreate(HealthRecordBase):
    animal_group_id: int
    group_type: str  # 'poultry', 'livestock', 'aquaculture'

class HealthRecordUpdate(HealthRecordBase):
    pass

class HealthRecordOut(HealthRecordBase):
    id: int
    animal_group_id: int
    group_type: str

    class Config:
        from_attributes = True


# ============================================================
# VETERINARY FILE UPLOAD
# ============================================================
class VeterinaryUploadBase(BaseModel):
    file_path: str
    file_type: str
    description: Optional[str] = None

class VeterinaryUploadCreate(VeterinaryUploadBase):
    recommendation_id: Optional[int] = None
    livestock_health_id: Optional[int] = None
    poultry_health_id: Optional[int] = None
    aquaculture_health_id: Optional[int] = None

class VeterinaryUploadOut(VeterinaryUploadBase):
    id: int
    recommendation_id: Optional[int]
    livestock_health_id: Optional[int]
    poultry_health_id: Optional[int]
    aquaculture_health_id: Optional[int]
    date_uploaded: date

    class Config:
        from_attributes = True


