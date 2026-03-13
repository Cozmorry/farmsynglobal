from sqlalchemy.orm import Session
from backend.modules.aquaculture import models, schemas

# ============================
# 🌊 PONDS SERVICES
# ============================
def create_pond(db: Session, pond: schemas.AquacultureCreate):
    db_item = models.Aquaculture(**pond.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_pond(db: Session, pond_id: int):
    return db.query(models.Aquaculture).filter(models.Aquaculture.id == pond_id).first()

def get_all_ponds(db: Session):
    return db.query(models.Aquaculture).all()

def update_pond(db: Session, pond_id: int, pond: schemas.AquacultureUpdate):
    db_item = db.query(models.Aquaculture).filter(models.Aquaculture.id == pond_id).first()
    if not db_item:
        return None
    for key, value in pond.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_pond(db: Session, pond_id: int):
    db_item = db.query(models.Aquaculture).filter(models.Aquaculture.id == pond_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# ============================
# 🍽 FEEDING SERVICES
# ============================
def create_feeding(db: Session, feeding: schemas.AquacultureFeedingCreate):
    db_item = models.AquacultureFeeding(**feeding.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_feedings(db: Session):
    return db.query(models.AquacultureFeeding).all()

def update_feeding(db: Session, feeding_id: int, feeding: schemas.AquacultureFeedingUpdate):
    db_item = db.query(models.AquacultureFeeding).filter(models.AquacultureFeeding.id == feeding_id).first()
    if not db_item:
        return None
    for key, value in feeding.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_feeding(db: Session, feeding_id: int):
    db_item = db.query(models.AquacultureFeeding).filter(models.AquacultureFeeding.id == feeding_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# ============================
# 💧 WATER QUALITY SERVICES
# ============================
def create_water_quality(db: Session, record: schemas.AquacultureWaterQualityCreate):
    db_item = models.AquacultureWaterQuality(**record.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_water_quality(db: Session):
    return db.query(models.AquacultureWaterQuality).all()

def update_water_quality(db: Session, record_id: int, record: schemas.AquacultureWaterQualityUpdate):
    db_item = db.query(models.AquacultureWaterQuality).filter(models.AquacultureWaterQuality.id == record_id).first()
    if not db_item:
        return None
    for key, value in record.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_water_quality(db: Session, record_id: int):
    db_item = db.query(models.AquacultureWaterQuality).filter(models.AquacultureWaterQuality.id == record_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# ============================
# 🐟 HARVEST SERVICES
# ============================
def create_harvest(db: Session, harvest: schemas.AquacultureHarvestCreate):
    db_item = models.AquacultureHarvest(**harvest.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_harvests(db: Session):
    return db.query(models.AquacultureHarvest).all()

def update_harvest(db: Session, harvest_id: int, harvest: schemas.AquacultureHarvestUpdate):
    db_item = db.query(models.AquacultureHarvest).filter(models.AquacultureHarvest.id == harvest_id).first()
    if not db_item:
        return None
    for key, value in harvest.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_harvest(db: Session, harvest_id: int):
    db_item = db.query(models.AquacultureHarvest).filter(models.AquacultureHarvest.id == harvest_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# ============================
# ⚡ ACTIVITY SERVICES
# ============================
def create_activity(db: Session, activity: schemas.AquacultureActivityCreate):
    db_item = models.AquacultureActivity(**activity.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_activities(db: Session):
    return db.query(models.AquacultureActivity).all()

def update_activity(db: Session, activity_id: int, activity: schemas.AquacultureActivityUpdate):
    db_item = db.query(models.AquacultureActivity).filter(models.AquacultureActivity.id == activity_id).first()
    if not db_item:
        return None
    for key, value in activity.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_activity(db: Session, activity_id: int):
    db_item = db.query(models.AquacultureActivity).filter(models.AquacultureActivity.id == activity_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# ============================
# 🎯 PRODUCTION SERVICES
# ============================
def create_production(db: Session, production: schemas.AquacultureProductionCreate):
    db_item = models.AquacultureProduction(**production.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_productions(db: Session):
    return db.query(models.AquacultureProduction).all()

def update_production(db: Session, production_id: int, production: schemas.AquacultureProductionUpdate):
    db_item = db.query(models.AquacultureProduction).filter(models.AquacultureProduction.id == production_id).first()
    if not db_item:
        return None
    for key, value in production.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_production(db: Session, production_id: int):
    db_item = db.query(models.AquacultureProduction).filter(models.AquacultureProduction.id == production_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# ============================
# 📊 SUMMARY SERVICES
# ============================
def create_summary(db: Session, summary: schemas.AquacultureSummaryCreate):
    db_item = models.AquacultureSummary(**summary.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_summaries(db: Session):
    return db.query(models.AquacultureSummary).all()

def update_summary(db: Session, summary_id: int, summary: schemas.AquacultureSummaryUpdate):
    db_item = db.query(models.AquacultureSummary).filter(models.AquacultureSummary.id == summary_id).first()
    if not db_item:
        return None
    for key, value in summary.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_summary(db: Session, summary_id: int):
    db_item = db.query(models.AquacultureSummary).filter(models.AquacultureSummary.id == summary_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item


