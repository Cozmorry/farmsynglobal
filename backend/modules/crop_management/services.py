# backend/modules/crop_management/services.py
from sqlalchemy.orm import Session
from typing import Optional, List, Type
from fastapi import HTTPException

from . import models, schemas

# ============================================================
# CROPS
# ============================================================

def create_crop(db: Session, crop_data: dict) -> schemas.CropRead:
    crop = models.Crop(**crop_data)
    db.add(crop)
    db.commit()
    db.refresh(crop)
    return schemas.CropRead.from_orm(crop)

def get_crops(db: Session, block_id: Optional[int] = None) -> List[schemas.CropRead]:
    query = db.query(models.Crop)
    if block_id is not None:
        query = query.filter(models.Crop.block_id == block_id)
    crops = query.all()
    return [schemas.CropRead.from_orm(c) for c in crops]

def get_crop(db: Session, crop_id: int) -> schemas.CropRead:
    crop = db.query(models.Crop).filter(models.Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return schemas.CropRead.from_orm(crop)

def update_crop(db: Session, crop_id: int, data: dict) -> schemas.CropRead:
    crop = db.query(models.Crop).filter(models.Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    for key, value in data.items():
        setattr(crop, key, value)
    db.commit()
    db.refresh(crop)
    return schemas.CropRead.from_orm(crop)

# ============================================================
# GENERIC ACTIVITIES
# ============================================================

def create_activity(db: Session, model: Type[models.Base], data: dict):
    record = model(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_activities(
    db: Session,
    model: Type[models.Base],
    crop_id: Optional[int] = None,
    block_id: Optional[int] = None,
):
    query = db.query(model)
    if crop_id is not None:
        query = query.filter(model.crop_id == crop_id)
    if block_id is not None:
        query = query.filter(model.block_id == block_id)
    return query.all()

def update_activity(
    db: Session,
    model: Type[models.Base],
    activity_id: int,
    data: dict,
):
    record = db.query(model).filter(model.id == activity_id).first()
    if not record:
        return None

    allowed_fields = {
        "date",
        "method",
        "description",
        "quantity",
        "quantity_kg",
        "quantity_ltr",
        "activity_type",
        "notes",
    }

    for key, value in data.items():
        if key in allowed_fields:
            setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record

def delete_activity(
    db: Session,
    model: Type[models.Base],
    activity_id: int,
):
    record = db.query(model).filter(model.id == activity_id).first()
    if not record:
        return None
    db.delete(record)
    db.commit()
    return True

# ============================================================
# HARVESTS
# ============================================================

def create_harvest(db: Session, data: dict) -> schemas.CropHarvestRead:
    harvest = models.CropHarvest(**data)
    db.add(harvest)
    db.commit()
    db.refresh(harvest)
    return schemas.CropHarvestRead.from_orm(harvest)

def get_harvest(db: Session, harvest_id: int) -> Optional[schemas.CropHarvestRead]:
    harvest = db.query(models.CropHarvest).filter(models.CropHarvest.id == harvest_id).first()
    if not harvest:
        return None
    return schemas.CropHarvestRead.from_orm(harvest)

def update_harvest(db: Session, harvest_id: int, data: dict) -> Optional[schemas.CropHarvestRead]:
    harvest = db.query(models.CropHarvest).filter(models.CropHarvest.id == harvest_id).first()
    if not harvest:
        return None
    for key, value in data.items():
        setattr(harvest, key, value)
    db.commit()
    db.refresh(harvest)
    return schemas.CropHarvestRead.from_orm(harvest)

def delete_harvest(db: Session, harvest_id: int) -> bool:
    harvest = db.query(models.CropHarvest).filter(models.CropHarvest.id == harvest_id).first()
    if not harvest:
        return False
    db.delete(harvest)
    db.commit()
    return True

# ============================================================
# SALES
# ============================================================

def create_sale(db: Session, data: dict) -> schemas.CropSaleRead:
    sale = models.CropSale(**data)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return schemas.CropSaleRead.from_orm(sale)

def get_sales(
    db: Session,
    crop_id: Optional[int] = None,
    block_id: Optional[int] = None,
) -> List[schemas.CropSaleRead]:
    query = db.query(models.CropSale)
    if crop_id is not None:
        query = query.filter(models.CropSale.crop_id == crop_id)
    if block_id is not None:
        query = query.filter(models.CropSale.block_id == block_id)
    return [schemas.CropSaleRead.from_orm(s) for s in query.all()]

# ============================================================
# ACTIVITY UPLOADS
# ============================================================

def normalize_activity_type(activity_type: str) -> str:
    return activity_type.replace("-", "_").replace("_activities", "").replace("_applications", "")

def upload_activity_file(
    db: Session,
    crop_id: int,
    activity_type: str,
    activity_id: int,
    file_path: str,
    file_type: str,
    description: Optional[str] = None,
) -> schemas.CropActivityUploadRead:
    crop = db.query(models.Crop).filter(models.Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop does not exist")

    normalized = normalize_activity_type(activity_type)

    activity_model_map = {
        "scouting": models.Scouting,
        "weeding": models.Weeding,
        "irrigation": models.Irrigation,
        "fertilizer": models.FertilizerApplication,
        "chemical": models.ChemicalApplication,
        "land_preparation": models.LandPreparation,
        "soil_test": models.SoilTest,
        "soil_amendment": models.SoilAmendment,
        "harvest": models.CropHarvest,
        "sale": models.CropSale,
        "nursery": models.NurseryActivity,
    }

    if normalized not in activity_model_map:
        raise HTTPException(status_code=400, detail=f"Invalid activity_type: {activity_type}")

    model = activity_model_map[normalized]

    activity = db.query(model).filter(model.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity record not found")

    upload = models.ActivityUpload(
        crop_id=crop_id,
        activity_type=normalized,
        activity_id=activity_id,
        file_path=file_path,
        file_type=file_type,
        description=description,
    )

    db.add(upload)
    db.commit()
    db.refresh(upload)

    return schemas.CropActivityUploadRead.from_orm(upload)

def get_activity_uploads(
    db: Session,
    crop_id: Optional[int] = None,
    activity_type: Optional[str] = None,
) -> List[schemas.CropActivityUploadRead]:
    query = db.query(models.ActivityUpload)

    if crop_id is not None:
        query = query.filter(models.ActivityUpload.crop_id == crop_id)

    if activity_type is not None:
        normalized = normalize_activity_type(activity_type)
        query = query.filter(models.ActivityUpload.activity_type == normalized)

    return [schemas.CropActivityUploadRead.from_orm(u) for u in query.all()]


