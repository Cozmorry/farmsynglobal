#backend/modules/veterinary/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.modules.veterinary import schemas, services

router = APIRouter(tags=["Veterinary"])

# ============================
# RECOMMENDATIONS
# ============================
@router.post("/recommendations/", response_model=schemas.VeterinaryRecommendationOut)
def create_recommendation(recommendation: schemas.VeterinaryRecommendationCreate, db: Session = Depends(get_db)):
    return services.create_recommendation(db, recommendation)

@router.get("/recommendations/{rec_id}", response_model=schemas.VeterinaryRecommendationOut)
def get_recommendation(rec_id: int, db: Session = Depends(get_db)):
    db_rec = services.get_recommendation(db, rec_id)
    if not db_rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return db_rec

@router.get("/recommendations/", response_model=List[schemas.VeterinaryRecommendationOut])
def list_recommendations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.list_recommendations(db, skip, limit)

@router.put("/recommendations/{rec_id}", response_model=schemas.VeterinaryRecommendationOut)
def update_recommendation(rec_id: int, rec_update: schemas.VeterinaryRecommendationUpdate, db: Session = Depends(get_db)):
    db_rec = services.update_recommendation(db, rec_id, rec_update)
    if not db_rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return db_rec

@router.delete("/recommendations/{rec_id}", response_model=schemas.VeterinaryRecommendationOut)
def delete_recommendation(rec_id: int, db: Session = Depends(get_db)):
    db_rec = services.delete_recommendation(db, rec_id)
    if not db_rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return db_rec

# ============================================================
# HEALTH RECORDS
# ============================================================
@router.get("/health/", response_model=List[schemas.HealthRecordOut])
def list_health(animal_group_id: int, group_type: str, db: Session = Depends(get_db)):
    try:
        return services.list_health_records(db, animal_group_id, group_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid group_type")

@router.post("/health/", response_model=schemas.HealthRecordOut)
def create_health(record: schemas.HealthRecordCreate, db: Session = Depends(get_db)):
    try:
        return services.create_health_record(db, record)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid group_type")

@router.put("/health/{record_id}", response_model=schemas.HealthRecordOut)
def update_health(record_id: int, record: schemas.HealthRecordUpdate, group_type: str, db: Session = Depends(get_db)):
    try:
        db_record = services.update_health_record(db, record_id, record, group_type)
        if not db_record:
            raise HTTPException(status_code=404, detail="Health record not found")
        return db_record
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid group_type")

@router.delete("/health/{record_id}", response_model=schemas.HealthRecordOut)
def delete_health(record_id: int, group_type: str, db: Session = Depends(get_db)):
    try:
        db_record = services.delete_health_record(db, record_id, group_type)
        if not db_record:
            raise HTTPException(status_code=404, detail="Health record not found")
        return db_record
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid group_type")

# ============================
# FILE UPLOADS
# ============================
@router.post("/uploads/", response_model=schemas.VeterinaryUploadOut)
def upload_file(upload: schemas.VeterinaryUploadCreate, db: Session = Depends(get_db)):
    return services.upload_veterinary_file(db, **upload.dict())

@router.get("/uploads/", response_model=List[schemas.VeterinaryUploadOut])
def get_uploads(
    recommendation_id: int = None,
    livestock_health_id: int = None,
    poultry_health_id: int = None,
    aquaculture_health_id: int = None,
    db: Session = Depends(get_db)
):
    return services.get_veterinary_uploads(
        db, recommendation_id, livestock_health_id, poultry_health_id, aquaculture_health_id
    )
