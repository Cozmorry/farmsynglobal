#backend/modules/poultry/services.py
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.modules.poultry import models, schemas
from datetime import date


# ============================================================
# 🐔 POULTRY BATCH SERVICES
# ============================================================

def create_batch(
    db: Session,
    batch: schemas.PoultryBatchCreate
) -> models.PoultryBatch:
    db_batch = models.PoultryBatch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch


def get_batch(
    db: Session,
    batch_id: int
) -> Optional[models.PoultryBatch]:
    return (
        db.query(models.PoultryBatch)
        .filter(models.PoultryBatch.id == batch_id)
        .first()
    )


def get_batches(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[models.PoultryBatch]:
    return (
        db.query(models.PoultryBatch)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_batch(
    db: Session,
    batch_id: int,
    batch_update: schemas.PoultryBatchUpdate
) -> Optional[models.PoultryBatch]:
    db_batch = get_batch(db, batch_id)
    if not db_batch:
        return None

    for field, value in batch_update.dict(exclude_unset=True).items():
        setattr(db_batch, field, value)

    db.commit()
    db.refresh(db_batch)
    return db_batch


def delete_batch(
    db: Session,
    batch_id: int
) -> bool:
    db_batch = get_batch(db, batch_id)
    if not db_batch:
        return False

    db.delete(db_batch)
    db.commit()
    return True


# ============================================================
# 📝 POULTRY ACTIVITY SERVICES (NO COST LOGIC)
# ============================================================

def create_activity(
    db: Session,
    activity: schemas.PoultryActivityCreate
) -> models.PoultryActivity:
    """
    Poultry records WHAT happened.
    Other modules decide WHAT IT COST.
    """

    db_activity = models.PoultryActivity(
        **activity.dict(),
        date=activity.date or date.today()
    )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity

    
def get_activity(
    db: Session,
    activity_id: int
) -> Optional[models.PoultryActivity]:
    return (
        db.query(models.PoultryActivity)
        .filter(models.PoultryActivity.id == activity_id)
        .first()
    )


def get_activities(
    db: Session,
    batch_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.PoultryActivity]:
    query = db.query(models.PoultryActivity)

    if batch_id:
        query = query.filter(
            models.PoultryActivity.poultry_batch_id == batch_id
        )

    return query.offset(skip).limit(limit).all()


def update_activity(
    db: Session,
    activity_id: int,
    activity_update: schemas.PoultryActivityUpdate
) -> Optional[models.PoultryActivity]:
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return None

    for field, value in activity_update.dict(exclude_unset=True).items():
        setattr(db_activity, field, value)

    db.commit()
    db.refresh(db_activity)
    return db_activity


def delete_activity(
    db: Session,
    activity_id: int
) -> bool:
    db_activity = get_activity(db, activity_id)
    if not db_activity:
        return False

    db.delete(db_activity)
    db.commit()
    return True


# ============================================================
# 🥚 POULTRY PRODUCTION SERVICES (NO FINANCE)
# ============================================================

def create_production(
    db: Session,
    production: schemas.PoultryProductionCreate
) -> models.PoultryProduction:
    db_prod = models.PoultryProduction(
        **production.dict(),
        date=production.date or date.today()
    )
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


def get_production(
    db: Session,
    production_id: int
) -> Optional[models.PoultryProduction]:
    return (
        db.query(models.PoultryProduction)
        .filter(models.PoultryProduction.id == production_id)
        .first()
    )


def get_productions(
    db: Session,
    batch_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.PoultryProduction]:
    query = db.query(models.PoultryProduction)

    if batch_id:
        query = query.filter(
            models.PoultryProduction.poultry_batch_id == batch_id
        )

    return query.offset(skip).limit(limit).all()


def update_production(
    db: Session,
    production_id: int,
    production_update: schemas.PoultryProductionUpdate
) -> Optional[models.PoultryProduction]:
    db_prod = get_production(db, production_id)
    if not db_prod:
        return None

    for field, value in production_update.dict(exclude_unset=True).items():
        setattr(db_prod, field, value)

    db.commit()
    db.refresh(db_prod)
    return db_prod


def delete_production(
    db: Session,
    production_id: int
) -> bool:
    db_prod = get_production(db, production_id)
    if not db_prod:
        return False

    db.delete(db_prod)
    db.commit()
    return True


# ============================================================
# 💰 POULTRY SALES SERVICES (FINANCE TRIGGER ONLY)
# ============================================================

def create_sale(
    db: Session,
    sale: schemas.PoultrySaleCreate
) -> models.PoultrySale:
    db_sale = models.PoultrySale(
        **sale.dict(),
        sale_date=sale.sale_date or date.today()
    )

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    return db_sale


def get_sale(
    db: Session,
    sale_id: int
) -> Optional[models.PoultrySale]:
    return (
        db.query(models.PoultrySale)
        .filter(models.PoultrySale.id == sale_id)
        .first()
    )


def get_sales(
    db: Session,
    batch_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.PoultrySale]:
    query = db.query(models.PoultrySale)

    if batch_id:
        query = query.filter(
            models.PoultrySale.poultry_batch_id == batch_id
        )

    return query.offset(skip).limit(limit).all()


def update_sale(
    db: Session,
    sale_id: int,
    sale_update: schemas.PoultrySaleUpdate
) -> Optional[models.PoultrySale]:
    db_sale = get_sale(db, sale_id)
    if not db_sale:
        return None

    for field, value in sale_update.dict(exclude_unset=True).items():
        setattr(db_sale, field, value)

    db.commit()
    db.refresh(db_sale)
    return db_sale


def delete_sale(
    db: Session,
    sale_id: int
) -> bool:
    db_sale = get_sale(db, sale_id)
    if not db_sale:
        return False

    db.delete(db_sale)
    db.commit()
    return True
