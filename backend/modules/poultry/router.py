# backend/modules/poultry/routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from backend.core.database import get_db
from backend.modules.poultry import services, schemas, models

router = APIRouter(tags=["Poultry"])

# ----------------------------
# Daily activity types (no store/health)
# ----------------------------
DAILY_ACTIVITY_TYPES = [
    "Feeding",
    "Watering",
    "Cleaning",
    "Egg Collection",
    "Observation / Behavior Check",
    "Lighting Adjustment",
    "Record Mortality",
]

# ----------------------------
# Helper functions
# ----------------------------
def create_daily_activities(db: Session, batch_id: int, performed_by: str = None):
    today = date.today()
    existing = db.query(models.PoultryActivity).filter(
        models.PoultryActivity.poultry_batch_id == batch_id,
        models.PoultryActivity.date == today
    ).all()

    if existing:
        return existing  # Avoid duplicates

    created_activities = []
    for activity_type in DAILY_ACTIVITY_TYPES:
        activity_data = schemas.PoultryActivityCreate(
            poultry_batch_id=batch_id,
            date=today,
            activity_type=activity_type,
            performed_by=performed_by,
           
            feed_used_kg=0.0 if activity_type == "Feeding" else None,
            water_used_l=0.0 if activity_type == "Watering" else None,
            mortality=0 if activity_type == "Record Mortality" else None,
        )
        activity = models.PoultryActivity(**activity_data.dict())
        db.add(activity)
        created_activities.append(activity)

    db.commit()
    for activity in created_activities:
        db.refresh(activity)
    return created_activities

def get_daily_summary(db: Session, batch_id: int, for_date: date = None):
    if not for_date:
        for_date = date.today()

    activities = db.query(models.PoultryActivity).filter(
        models.PoultryActivity.poultry_batch_id == batch_id,
        models.PoultryActivity.date == for_date
    ).all()

    summary = {
        "date": for_date,
        "batch_id": batch_id,
        "total_feed_kg": sum(a.feed_used_kg or 0 for a in activities),
        "total_water_l": sum(a.water_used_l or 0 for a in activities),
        "total_mortality": sum(a.mortality or 0 for a in activities),
    }
    return summary

# ----------------------------
# Poultry Batch Routes
# ----------------------------
@router.post("/batches/", response_model=schemas.PoultryBatchRead)
def create_batch(batch: schemas.PoultryBatchCreate, db: Session = Depends(get_db)):
    return services.create_batch(db, batch)

@router.get("/batches/{batch_id}", response_model=schemas.PoultryBatchRead)
def read_batch(batch_id: int, db: Session = Depends(get_db)):
    db_batch = services.get_batch(db, batch_id)
    if not db_batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return db_batch

@router.get("/batches/", response_model=List[schemas.PoultryBatchRead])
def read_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_batches(db, skip=skip, limit=limit)

@router.put("/batches/{batch_id}", response_model=schemas.PoultryBatchRead)
def update_batch(batch_id: int, batch_update: schemas.PoultryBatchUpdate, db: Session = Depends(get_db)):
    db_batch = services.update_batch(db, batch_id, batch_update)
    if not db_batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return db_batch

@router.delete("/batches/{batch_id}")
def delete_batch(batch_id: int, db: Session = Depends(get_db)):
    success = services.delete_batch(db, batch_id)
    if not success:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"detail": "Batch deleted successfully"}

# ----------------------------
# Poultry Activity Routes
# ----------------------------
@router.post("/activities/", response_model=schemas.PoultryActivityRead)
def create_activity(activity: schemas.PoultryActivityCreate, db: Session = Depends(get_db)):
    return services.create_activity(db, activity)

@router.get("/activities/{activity_id}", response_model=schemas.PoultryActivityRead)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = services.get_activity(db, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@router.get("/activities/", response_model=List[schemas.PoultryActivityRead])
def read_activities(batch_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_activities(db, batch_id=batch_id, skip=skip, limit=limit)

@router.put("/activities/{activity_id}", response_model=schemas.PoultryActivityRead)
def update_activity(activity_id: int, activity_update: schemas.PoultryActivityUpdate, db: Session = Depends(get_db)):
    db_activity = services.update_activity(db, activity_id, activity_update)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@router.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    success = services.delete_activity(db, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"detail": "Activity deleted successfully"}

# ----------------------------
# Daily Auto Activities
# ----------------------------
@router.post("/batches/{batch_id}/daily-activities", response_model=List[schemas.PoultryActivityRead])
def create_daily_activities_endpoint(batch_id: int, performed_by: str = None, db: Session = Depends(get_db)):
    batch = services.get_batch(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return create_daily_activities(db, batch_id, performed_by)

@router.get("/batches/{batch_id}/daily-summary")
def get_daily_summary_endpoint(batch_id: int, for_date: date = None, db: Session = Depends(get_db)):
    batch = services.get_batch(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return get_daily_summary(db, batch_id, for_date)

# ----------------------------
# Poultry Production Routes
# ----------------------------
@router.post("/production/", response_model=schemas.PoultryProductionRead)
def create_production(production: schemas.PoultryProductionCreate, db: Session = Depends(get_db)):
    return services.create_production(db, production)

@router.get("/production/{production_id}", response_model=schemas.PoultryProductionRead)
def read_production(production_id: int, db: Session = Depends(get_db)):
    db_prod = services.get_production(db, production_id)
    if not db_prod:
        raise HTTPException(status_code=404, detail="Production not found")
    return db_prod

@router.get("/production/", response_model=List[schemas.PoultryProductionRead])
def read_productions(batch_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_productions(db, batch_id=batch_id, skip=skip, limit=limit)

@router.put("/production/{production_id}", response_model=schemas.PoultryProductionRead)
def update_production(production_id: int, production_update: schemas.PoultryProductionUpdate, db: Session = Depends(get_db)):
    db_prod = services.update_production(db, production_id, production_update)
    if not db_prod:
        raise HTTPException(status_code=404, detail="Production not found")
    return db_prod

@router.delete("/production/{production_id}")
def delete_production(production_id: int, db: Session = Depends(get_db)):
    success = services.delete_production(db, production_id)
    if not success:
        raise HTTPException(status_code=404, detail="Production not found")
    return {"detail": "Production deleted successfully"}

# ----------------------------
# Poultry Sales Routes
# ----------------------------
@router.post("/sales/", response_model=schemas.PoultrySaleRead)
def create_sale(sale: schemas.PoultrySaleCreate, db: Session = Depends(get_db)):
    return services.create_sale(db, sale)

@router.get("/sales/{sale_id}", response_model=schemas.PoultrySaleRead)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = services.get_sale(db, sale_id)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.get("/sales/", response_model=List[schemas.PoultrySaleRead])
def read_sales(batch_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_sales(db, batch_id=batch_id, skip=skip, limit=limit)

@router.put("/sales/{sale_id}", response_model=schemas.PoultrySaleRead)
def update_sale(sale_id: int, sale_update: schemas.PoultrySaleUpdate, db: Session = Depends(get_db)):
    db_sale = services.update_sale(db, sale_id, sale_update)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    success = services.delete_sale(db, sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {"detail": "Sale deleted successfully"}




# ============================================================
# 🧮 POULTRY BATCH SUMMARY ROUTE
# ============================================================

@router.get("/batches/{batch_id}/summary")
def batch_summary(batch_id: int, db: Session = Depends(get_db)):
    batch = services.get_batch(db, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    return {
        "batch_id": batch.id,
        "batch_name": batch.batch_name,
        "total_eggs": sum(
            p.quantity for p in batch.productions
            if p.production_type.lower() == "egg"
        ),
        "total_sales_amount": sum(
            s.quantity * s.unit_price for s in batch.sales
        ),
        "total_mortality": sum(a.mortality or 0 for a in batch.activities),
        "total_feed_used_kg": sum(a.feed_used_kg or 0 for a in batch.activities),
        "total_water_used_l": sum(a.water_used_l or 0 for a in batch.activities),
    }
