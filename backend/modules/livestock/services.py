# backend/modules/livestock/services.py

from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException

from backend.modules.livestock import models, schemas

# =====================================================
# LIVESTOCK CRUD
# =====================================================
def create_livestock(db: Session, livestock: schemas.LivestockCreate) -> models.Livestock:
    db_livestock = models.Livestock(**livestock.dict())
    db.add(db_livestock)
    db.commit()
    db.refresh(db_livestock)
    return db_livestock


def get_all_livestock(db: Session) -> List[models.Livestock]:
    return db.query(models.Livestock).all()


def get_livestock(db: Session, livestock_id: int) -> models.Livestock:
    livestock = db.query(models.Livestock).filter(models.Livestock.id == livestock_id).first()
    if not livestock:
        raise HTTPException(status_code=404, detail="Livestock not found")
    return livestock


def update_livestock(db: Session, livestock_id: int, livestock: schemas.LivestockUpdate) -> models.Livestock:
    db_livestock = get_livestock(db, livestock_id)
    for key, value in livestock.dict(exclude_unset=True).items():
        setattr(db_livestock, key, value)
    db.commit()
    db.refresh(db_livestock)
    return db_livestock


def delete_livestock(db: Session, livestock_id: int):
    db_livestock = get_livestock(db, livestock_id)
    db.delete(db_livestock)
    db.commit()
    return {"detail": "Livestock deleted successfully"}


# =====================================================
# LIVESTOCK GROUP / HERD
# =====================================================
def create_group(db: Session, group: schemas.LivestockGroupCreate) -> models.LivestockGroup:
    db_group = models.LivestockGroup(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_all_groups(db: Session) -> List[models.LivestockGroup]:
    return db.query(models.LivestockGroup).all()


def assign_to_group(db: Session, livestock_id: int, group_id: int):
    livestock = get_livestock(db, livestock_id)
    livestock.group_id = group_id
    db.commit()
    db.refresh(livestock)
    return livestock


# =====================================================
# WEIGHT RECORDS
# =====================================================
def create_weight(db: Session, weight: schemas.LivestockWeightRecordCreate) -> models.LivestockWeightRecord:
    db_weight = models.LivestockWeightRecord(**weight.dict())
    db.add(db_weight)
    db.commit()
    db.refresh(db_weight)
    return db_weight


def get_all_weights(db: Session) -> List[models.LivestockWeightRecord]:
    return db.query(models.LivestockWeightRecord).all()


# =====================================================
# FEEDING (INDIVIDUAL OR GROUP)
# =====================================================
def create_feeding(db: Session, feeding: schemas.LivestockFeedingCreate) -> models.LivestockFeeding:
    db_feeding = models.LivestockFeeding(**feeding.dict())
    db.add(db_feeding)
    db.commit()
    db.refresh(db_feeding)
    return db_feeding


def get_all_feeding(db: Session) -> List[models.LivestockFeeding]:
    return db.query(models.LivestockFeeding).all()


# =====================================================
# ACTIVITIES
# =====================================================
def create_activity(db: Session, activity: schemas.LivestockActivityCreate) -> models.LivestockActivity:
    db_activity = models.LivestockActivity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def get_all_activities(db: Session) -> List[models.LivestockActivity]:
    return db.query(models.LivestockActivity).all()


# =====================================================
# BREEDING
# =====================================================
def create_breeding(db: Session, breeding: schemas.LivestockBreedingCreate) -> models.LivestockBreeding:
    db_breeding = models.LivestockBreeding(**breeding.dict())
    db.add(db_breeding)
    db.commit()
    db.refresh(db_breeding)
    return db_breeding


def get_all_breeding(db: Session) -> List[models.LivestockBreeding]:
    return db.query(models.LivestockBreeding).all()


def get_breeding_as_dam(db: Session, livestock_id: int) -> List[models.LivestockBreeding]:
    return db.query(models.LivestockBreeding).filter(models.LivestockBreeding.dam_id == livestock_id).all()


def get_breeding_as_sire(db: Session, livestock_id: int) -> List[models.LivestockBreeding]:
    return db.query(models.LivestockBreeding).filter(models.LivestockBreeding.sire_id == livestock_id).all()


# =====================================================
# PRODUCTION
# =====================================================
def create_production(db: Session, production: schemas.LivestockProductionCreate) -> models.LivestockProduction:
    db_production = models.LivestockProduction(**production.dict())
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production


def get_all_productions(db: Session) -> List[models.LivestockProduction]:
    return db.query(models.LivestockProduction).all()


# =====================================================
# SALES
# =====================================================
def create_sale(db: Session, sale: schemas.LivestockSaleCreate) -> models.LivestockSale:
    data = sale.dict()
    data["total_sale"] = data["quantity"] * data["unit_price"]
    db_sale = models.LivestockSale(**data)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


def get_all_sales(db: Session) -> List[models.LivestockSale]:
    return db.query(models.LivestockSale).all()


# =====================================================
# LIFECYCLE STATUS TRANSITIONS
# =====================================================
def transition_livestock_status(db: Session, livestock_id: int, new_status: models.LivestockStatusEnum) -> models.Livestock:
    livestock = get_livestock(db, livestock_id)

    if livestock.status != models.LivestockStatusEnum.ACTIVE:
        raise HTTPException(status_code=400, detail="Only ACTIVE livestock can change status")

    if new_status not in [
        models.LivestockStatusEnum.SOLD,
        models.LivestockStatusEnum.SLAUGHTERED,
        models.LivestockStatusEnum.DECEASED,
    ]:
        raise HTTPException(status_code=400, detail="Invalid status transition")

    livestock.status = new_status
    db.commit()
    db.refresh(livestock)
    return livestock
