# backend/modules/veterinary/services.py
from sqlalchemy.orm import Session
from backend.modules.veterinary import models, schemas

# ============================================================
# RECOMMENDATIONS CRUD
# ============================================================
def create_recommendation(db: Session, recommendation: schemas.VeterinaryRecommendationCreate):
    db_rec = models.VeterinaryRecommendation(
        recommendation_text=recommendation.recommendation_text,
        recommended_action=recommendation.recommended_action,
        date_given=recommendation.date_given or None,
        livestock_health_id=recommendation.livestock_health_id,
        poultry_health_id=recommendation.poultry_health_id,
        aquaculture_health_id=recommendation.aquaculture_health_id,
        animal_group_id=recommendation.animal_group_id,
    )
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    return db_rec

def get_recommendation(db: Session, rec_id: int):
    return db.query(models.VeterinaryRecommendation).filter(models.VeterinaryRecommendation.id == rec_id).first()

def list_recommendations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VeterinaryRecommendation).offset(skip).limit(limit).all()

def update_recommendation(db: Session, rec_id: int, rec_update: schemas.VeterinaryRecommendationUpdate):
    db_rec = get_recommendation(db, rec_id)
    if not db_rec:
        return None
    for field, value in rec_update.dict(exclude_unset=True).items():
        setattr(db_rec, field, value)
    db.commit()
    db.refresh(db_rec)
    return db_rec

def delete_recommendation(db: Session, rec_id: int):
    db_rec = get_recommendation(db, rec_id)
    if not db_rec:
        return None
    db.delete(db_rec)
    db.commit()
    return db_rec

# ============================================================
# HELPER: select correct model based on group_type
# ============================================================
def get_health_model(group_type: str):
    if group_type.lower() == "poultry":
        return models.PoultryHealth
    elif group_type.lower() == "livestock":
        return models.LivestockHealth
    elif group_type.lower() == "aquaculture":
        return models.AquacultureHealth
    else:
        raise ValueError("Invalid group_type")

# ============================================================
# LIST HEALTH RECORDS
# ============================================================
def list_health_records(db: Session, animal_group_id: int, group_type: str):
    model = get_health_model(group_type)
    return db.query(model).filter(model.animal_group_id == animal_group_id).all()

# ============================================================
# CREATE HEALTH RECORD
# ============================================================
def create_health_record(db: Session, record: schemas.HealthRecordCreate):
    model = get_health_model(record.group_type)
    db_record = model(
        animal_group_id=record.animal_group_id,
        date_checked=record.date_checked,
        symptoms=record.symptoms,
        mortality=record.mortality,
        disease_detected=record.disease_detected,
        treatment_given=record.treatment_given,
        health_status=record.health_status,
        notes=record.notes,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# ============================================================
# UPDATE HEALTH RECORD
# ============================================================
def update_health_record(db: Session, record_id: int, record_update: schemas.HealthRecordUpdate, group_type: str):
    model = get_health_model(group_type)
    db_record = db.query(model).filter(model.id == record_id).first()
    if not db_record:
        return None
    for field, value in record_update.dict(exclude_unset=True).items():
        setattr(db_record, field, value)
    db.commit()
    db.refresh(db_record)
    return db_record

# ============================================================
# DELETE HEALTH RECORD
# ============================================================
def delete_health_record(db: Session, record_id: int, group_type: str):
    model = get_health_model(group_type)
    db_record = db.query(model).filter(model.id == record_id).first()
    if not db_record:
        return None
    db.delete(db_record)
    db.commit()
    return db_record


# ============================================================
# FILE UPLOADS
# ============================================================
def upload_veterinary_file(
    db: Session,
    file_path: str,
    file_type: str,
    recommendation_id: int = None,
    livestock_health_id: int = None,
    poultry_health_id: int = None,
    aquaculture_health_id: int = None,
    description: str = None
):
    upload = models.VeterinaryUpload(
        file_path=file_path,
        file_type=file_type,
        description=description,
        recommendation_id=recommendation_id,
        livestock_health_id=livestock_health_id,
        poultry_health_id=poultry_health_id,
        aquaculture_health_id=aquaculture_health_id
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload

def get_veterinary_uploads(
    db: Session,
    recommendation_id: int = None,
    livestock_health_id: int = None,
    poultry_health_id: int = None,
    aquaculture_health_id: int = None
):
    query = db.query(models.VeterinaryUpload)
    if recommendation_id:
        query = query.filter(models.VeterinaryUpload.recommendation_id == recommendation_id)
    if livestock_health_id:
        query = query.filter(models.VeterinaryUpload.livestock_health_id == livestock_health_id)
    if poultry_health_id:
        query = query.filter(models.VeterinaryUpload.poultry_health_id == poultry_health_id)
    if aquaculture_health_id:
        query = query.filter(models.VeterinaryUpload.aquaculture_health_id == aquaculture_health_id)
    return query.all()


