#backend/modules/aquaculture/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.modules.aquaculture import schemas, services

router = APIRouter(tags=["Aquaculture"])

# ============================
# 🌊 PONDS ROUTES
# ============================
@router.post("/ponds/", response_model=schemas.AquacultureRead)
def create_pond(pond: schemas.AquacultureCreate, db: Session = Depends(get_db)):
    return services.create_pond(db, pond)

@router.get("/ponds/", response_model=List[schemas.AquacultureRead])
def get_ponds(db: Session = Depends(get_db)):
    return services.get_all_ponds(db)

@router.get("/ponds/{pond_id}", response_model=schemas.AquacultureRead)
def get_pond(pond_id: int, db: Session = Depends(get_db)):
    pond = services.get_pond(db, pond_id)
    if not pond:
        raise HTTPException(status_code=404, detail="Pond not found")
    return pond

@router.put("/ponds/{pond_id}", response_model=schemas.AquacultureRead)
def update_pond(pond_id: int, pond: schemas.AquacultureUpdate, db: Session = Depends(get_db)):
    updated = services.update_pond(db, pond_id, pond)
    if not updated:
        raise HTTPException(status_code=404, detail="Pond not found")
    return updated

@router.delete("/ponds/{pond_id}")
def delete_pond(pond_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_pond(db, pond_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pond not found")
    return {"detail": "Pond deleted successfully"}

# ============================
# 🍽 FEEDINGS ROUTES
# ============================
@router.post("/feedings/", response_model=schemas.AquacultureFeedingRead)
def create_feeding(feeding: schemas.AquacultureFeedingCreate, db: Session = Depends(get_db)):
    return services.create_feeding(db, feeding)

@router.get("/feedings/", response_model=List[schemas.AquacultureFeedingRead])
def get_feedings(db: Session = Depends(get_db)):
    return services.get_all_feedings(db)

@router.put("/feedings/{feeding_id}", response_model=schemas.AquacultureFeedingRead)
def update_feeding(feeding_id: int, feeding: schemas.AquacultureFeedingUpdate, db: Session = Depends(get_db)):
    updated = services.update_feeding(db, feeding_id, feeding)
    if not updated:
        raise HTTPException(status_code=404, detail="Feeding record not found")
    return updated

@router.delete("/feedings/{feeding_id}")
def delete_feeding(feeding_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_feeding(db, feeding_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Feeding record not found")
    return {"detail": "Feeding record deleted successfully"}

# ============================
# 💧 WATER QUALITY ROUTES
# ============================
@router.post("/water_quality/", response_model=schemas.AquacultureWaterQualityRead)
def create_water_quality(record: schemas.AquacultureWaterQualityCreate, db: Session = Depends(get_db)):
    return services.create_water_quality(db, record)

@router.get("/water_quality/", response_model=List[schemas.AquacultureWaterQualityRead])
def get_water_quality(db: Session = Depends(get_db)):
    return services.get_all_water_quality(db)

@router.put("/water_quality/{record_id}", response_model=schemas.AquacultureWaterQualityRead)
def update_water_quality(record_id: int, record: schemas.AquacultureWaterQualityUpdate, db: Session = Depends(get_db)):
    updated = services.update_water_quality(db, record_id, record)
    if not updated:
        raise HTTPException(status_code=404, detail="Water quality record not found")
    return updated

@router.delete("/water_quality/{record_id}")
def delete_water_quality(record_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_water_quality(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Water quality record not found")
    return {"detail": "Water quality record deleted successfully"}

# ============================
# 🐟 HARVEST ROUTES
# ============================
@router.post("/harvests/", response_model=schemas.AquacultureHarvestRead)
def create_harvest(harvest: schemas.AquacultureHarvestCreate, db: Session = Depends(get_db)):
    return services.create_harvest(db, harvest)

@router.get("/harvests/", response_model=List[schemas.AquacultureHarvestRead])
def get_harvests(db: Session = Depends(get_db)):
    return services.get_all_harvests(db)

@router.put("/harvests/{harvest_id}", response_model=schemas.AquacultureHarvestRead)
def update_harvest(harvest_id: int, harvest: schemas.AquacultureHarvestUpdate, db: Session = Depends(get_db)):
    updated = services.update_harvest(db, harvest_id, harvest)
    if not updated:
        raise HTTPException(status_code=404, detail="Harvest record not found")
    return updated

@router.delete("/harvests/{harvest_id}")
def delete_harvest(harvest_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_harvest(db, harvest_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Harvest record not found")
    return {"detail": "Harvest record deleted successfully"}

# ============================
# ⚡ ACTIVITIES ROUTES
# ============================
@router.post("/activities/", response_model=schemas.AquacultureActivityRead)
def create_activity(activity: schemas.AquacultureActivityCreate, db: Session = Depends(get_db)):
    return services.create_activity(db, activity)

@router.get("/activities/", response_model=List[schemas.AquacultureActivityRead])
def get_activities(db: Session = Depends(get_db)):
    return services.get_all_activities(db)

@router.put("/activities/{activity_id}", response_model=schemas.AquacultureActivityRead)
def update_activity(activity_id: int, activity: schemas.AquacultureActivityUpdate, db: Session = Depends(get_db)):
    updated = services.update_activity(db, activity_id, activity)
    if not updated:
        raise HTTPException(status_code=404, detail="Activity record not found")
    return updated

@router.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_activity(db, activity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Activity record not found")
    return {"detail": "Activity record deleted successfully"}

# ============================
# 🎯 PRODUCTIONS ROUTES
# ============================
@router.post("/productions/", response_model=schemas.AquacultureProductionRead)
def create_production(production: schemas.AquacultureProductionCreate, db: Session = Depends(get_db)):
    return services.create_production(db, production)

@router.get("/productions/", response_model=List[schemas.AquacultureProductionRead])
def get_productions(db: Session = Depends(get_db)):
    return services.get_all_productions(db)

@router.put("/productions/{production_id}", response_model=schemas.AquacultureProductionRead)
def update_production(production_id: int, production: schemas.AquacultureProductionUpdate, db: Session = Depends(get_db)):
    updated = services.update_production(db, production_id, production)
    if not updated:
        raise HTTPException(status_code=404, detail="Production record not found")
    return updated

@router.delete("/productions/{production_id}")
def delete_production(production_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_production(db, production_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Production record not found")
    return {"detail": "Production record deleted successfully"}

# ============================
# 📊 SUMMARIES ROUTES
# ============================
@router.post("/summaries/", response_model=schemas.AquacultureSummaryRead)
def create_summary(summary: schemas.AquacultureSummaryCreate, db: Session = Depends(get_db)):
    return services.create_summary(db, summary)

@router.get("/summaries/", response_model=List[schemas.AquacultureSummaryRead])
def get_summaries(db: Session = Depends(get_db)):
    return services.get_all_summaries(db)

@router.put("/summaries/{summary_id}", response_model=schemas.AquacultureSummaryRead)
def update_summary(summary_id: int, summary: schemas.AquacultureSummaryUpdate, db: Session = Depends(get_db)):
    updated = services.update_summary(db, summary_id, summary)
    if not updated:
        raise HTTPException(status_code=404, detail="Summary record not found")
    return updated

@router.delete("/summaries/{summary_id}")
def delete_summary(summary_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_summary(db, summary_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Summary record not found")
    return {"detail": "Summary record deleted successfully"}



