#backend/modules/crop_management/router.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os

from backend.core.database import get_db
from backend.modules.crop_management import services, models, schemas

router = APIRouter(tags=["Crop Management"])

# ============================================================
# CROPS
# ============================================================

@router.post("/crops/", response_model=schemas.CropRead)
def create_crop(crop: schemas.CropCreate, db: Session = Depends(get_db)):
    return services.create_crop(db, crop.dict())

@router.get("/crops/", response_model=List[schemas.CropRead])
def list_crops(block_id: Optional[int] = None, db: Session = Depends(get_db)):
    return services.get_crops(db, block_id)

@router.get("/crops/{crop_id}", response_model=schemas.CropRead)
def get_crop(crop_id: int, db: Session = Depends(get_db)):
    return services.get_crop(db, crop_id)

@router.put("/crops/{crop_id}", response_model=schemas.CropRead)
def update_crop(crop_id: int, crop: schemas.CropCreate, db: Session = Depends(get_db)):
    return services.update_crop(db, crop_id, crop.dict())

# ============================================================
# GENERIC ACTIVITIES
# ============================================================

activity_map = [
    ("general-activities", models.CropActivity, schemas.CropActivityRead, schemas.CropActivityCreate),
    ("nursery-activities", models.NurseryActivity, schemas.NurseryActivityRead, schemas.NurseryActivityCreate),
    ("land-preparations", models.LandPreparation, schemas.LandPreparationActivityRead, schemas.LandPreparationActivityCreate),
    ("irrigations", models.Irrigation, schemas.IrrigationRead, schemas.IrrigationCreate),
    ("fertilizer-applications", models.FertilizerApplication, schemas.FertilizerApplicationRead, schemas.FertilizerApplicationCreate),
    ("chemical-applications", models.ChemicalApplication, schemas.ChemicalApplicationRead, schemas.ChemicalApplicationCreate),
    ("weeding-activities", models.Weeding, schemas.WeedingActivityRead, schemas.WeedingActivityCreate),
    ("scouting-activities", models.Scouting, schemas.ScoutingActivityRead, schemas.ScoutingActivityCreate),
    ("soil-tests", models.SoilTest, schemas.SoilTestRead, schemas.SoilTestCreate),
    ("soil-amendments", models.SoilAmendment, schemas.SoilAmendmentRead, schemas.SoilAmendmentCreate),
    ("crop-rotations", models.CropRotation, schemas.CropRotationRead, schemas.CropRotationCreate),
]

# Factory function to register each activity type
def register_activity_routes(prefix, model, read_schema, create_schema):
    # CREATE
    async def create_func(data: create_schema, db: Session = Depends(get_db)):
        return services.create_activity(db, model, data.dict())

    # LIST
    async def list_func(crop_id: Optional[int] = None, block_id: Optional[int] = None, db: Session = Depends(get_db)):
        records = services.get_activities(db, model, crop_id, block_id)
        return [read_schema.from_orm(r) for r in records]

    # UPDATE
    async def update_func(activity_id: int, data: create_schema, db: Session = Depends(get_db)):
        updated = services.update_activity(db, model, activity_id, data.dict())
        if not updated:
            raise HTTPException(status_code=404, detail=f"{prefix} record not found")
        return read_schema.from_orm(updated)

    # DELETE
    async def delete_func(activity_id: int, db: Session = Depends(get_db)):
        deleted = services.delete_activity(db, model, activity_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"{prefix} record not found")
        return {"message": "Deleted successfully"}

    router.post(f"/activities/{prefix}/", response_model=read_schema)(create_func)
    router.get(f"/activities/{prefix}/", response_model=List[read_schema])(list_func)
    router.put(f"/activities/{prefix}/{{activity_id}}", response_model=read_schema)(update_func)
    router.delete(f"/activities/{prefix}/{{activity_id}}")(delete_func)

# Register all activity routes
for prefix, model, read_schema, create_schema in activity_map:
    register_activity_routes(prefix, model, read_schema, create_schema)

# ============================================================
# HARVESTS
# ============================================================

@router.get("/harvests/{harvest_id}", response_model=schemas.CropHarvestRead)
def get_harvest(harvest_id: int, db: Session = Depends(get_db)):
    harvest = services.get_harvest(db, harvest_id)
    if not harvest:
        raise HTTPException(status_code=404, detail="Harvest not found")
    return harvest

@router.put("/harvests/{harvest_id}", response_model=schemas.CropHarvestRead)
def update_harvest(harvest_id: int, harvest: schemas.CropHarvestCreate, db: Session = Depends(get_db)):
    updated = services.update_harvest(db, harvest_id, harvest.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Harvest not found")
    return updated

@router.delete("/harvests/{harvest_id}")
def delete_harvest(harvest_id: int, db: Session = Depends(get_db)):
    if not services.delete_harvest(db, harvest_id):
        raise HTTPException(status_code=404, detail="Harvest not found")
    return {"message": "Deleted successfully"}

# ============================================================
# SALES
# ============================================================

@router.post("/sales/", response_model=schemas.CropSaleRead)
def create_sale(sale: schemas.CropSaleCreate, db: Session = Depends(get_db)):
    return services.create_sale(db, sale.dict())

@router.get("/sales/", response_model=List[schemas.CropSaleRead])
def list_sales(crop_id: Optional[int] = None, block_id: Optional[int] = None, db: Session = Depends(get_db)):
    return services.get_sales(db, crop_id, block_id)

# ============================================================
# ACTIVITY UPLOADS
# ============================================================

@router.post("/uploads/", response_model=schemas.CropActivityUploadRead)
async def upload_activity_file(
    crop_id: int = Form(...),
    activity_type: str = Form(...),
    activity_id: int = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    upload_dir = "uploads/activity_files"
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    ext = os.path.splitext(file.filename)[1]
    filename = f"{activity_type}_{activity_id}_{timestamp}{ext}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return services.upload_activity_file(
        db=db,
        crop_id=crop_id,
        activity_type=activity_type.lower(),
        activity_id=activity_id,
        file_path=file_path,
        file_type=file.content_type,
        description=description,
    )


@router.get("/uploads/", response_model=List[schemas.CropActivityUploadRead])
def list_uploads(
    crop_id: Optional[int] = None,
    activity_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return services.get_activity_uploads(db, crop_id, activity_type)

