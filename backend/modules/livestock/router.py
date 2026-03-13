# backend/modules/livestock/router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.modules.livestock import schemas, services

router = APIRouter(tags=["Livestock"])

# -----------------------------
# LIVESTOCK CRUD
# -----------------------------

@router.post("/", response_model=schemas.LivestockRead)
def create_livestock(livestock: schemas.LivestockCreate, db: Session = Depends(get_db)):
    """
    Create a new livestock entry.
    """
    return services.create_livestock(db, livestock)


@router.get("/", response_model=List[schemas.LivestockRead])
def get_all_livestock(db: Session = Depends(get_db)):
    """
    Get all livestock in the farm.
    """
    return services.get_all_livestock(db)


@router.get("/{livestock_id}", response_model=schemas.LivestockRead)
def get_livestock(livestock_id: int, db: Session = Depends(get_db)):
    """
    Get a single livestock by ID.
    """
    return services.get_livestock(db, livestock_id)


@router.put("/{livestock_id}", response_model=schemas.LivestockRead)
def update_livestock(livestock_id: int, livestock: schemas.LivestockUpdate, db: Session = Depends(get_db)):
    """
    Update an existing livestock's details.
    """
    return services.update_livestock(db, livestock_id, livestock)


@router.delete("/{livestock_id}")
def delete_livestock(livestock_id: int, db: Session = Depends(get_db)):
    """
    Delete a livestock by ID.
    """
    return services.delete_livestock(db, livestock_id)


# -----------------------------
# LIVESTOCK GROUPS / HERDS
# -----------------------------

@router.post("/groups/", response_model=schemas.LivestockGroupRead)
def create_group(group: schemas.LivestockGroupCreate, db: Session = Depends(get_db)):
    """
    Create a livestock group/herd.
    """
    return services.create_group(db, group)


@router.get("/groups/", response_model=List[schemas.LivestockGroupRead])
def get_all_groups(db: Session = Depends(get_db)):
    """
    Get all livestock groups/herds.
    """
    return services.get_all_groups(db)


@router.put("/groups/{group_id}/assign/{livestock_id}", response_model=schemas.LivestockRead)
def assign_to_group(group_id: int, livestock_id: int, db: Session = Depends(get_db)):
    """
    Assign a livestock to a specific group/herd.
    """
    return services.assign_to_group(db, livestock_id, group_id)

# -----------------------------
# BREEDING
# -----------------------------

@router.post("/breeding/", response_model=schemas.LivestockBreedingRead)
def create_breeding(
    breeding: schemas.LivestockBreedingCreate,
    db: Session = Depends(get_db)
):
    """
    Record a breeding / service event.
    """
    return services.create_breeding(db, breeding)


@router.get("/breeding/", response_model=List[schemas.LivestockBreedingRead])
def get_all_breeding(db: Session = Depends(get_db)):
    """
    Get all breeding records.
    """
    return services.get_all_breeding(db)


@router.get("/breeding/dam/{livestock_id}", response_model=List[schemas.LivestockBreedingRead])
def get_breeding_as_dam(livestock_id: int, db: Session = Depends(get_db)):
    """
    Get breeding records where livestock is dam.
    """
    return services.get_breeding_as_dam(db, livestock_id)


@router.get("/breeding/sire/{livestock_id}", response_model=List[schemas.LivestockBreedingRead])
def get_breeding_as_sire(livestock_id: int, db: Session = Depends(get_db)):
    """
    Get breeding records where livestock is sire.
    """
    return services.get_breeding_as_sire(db, livestock_id)



# -----------------------------
# WEIGHT RECORDS
# -----------------------------

@router.post("/weights/", response_model=schemas.LivestockWeightRecordRead)
def create_weight(weight: schemas.LivestockWeightRecordCreate, db: Session = Depends(get_db)):
    """
    Record weight for a livestock.
    """
    return services.create_weight(db, weight)


@router.get("/weights/", response_model=List[schemas.LivestockWeightRecordRead])
def get_all_weights(db: Session = Depends(get_db)):
    """
    Get all livestock weight records.
    """
    return services.get_all_weights(db)


# -----------------------------
# PRODUCTION
# -----------------------------

@router.post("/productions/", response_model=schemas.LivestockProductionRead)
def create_production(production: schemas.LivestockProductionCreate, db: Session = Depends(get_db)):
    """
    Record livestock production (milk, meat, eggs, etc.).
    """
    return services.create_production(db, production)


@router.get("/productions/", response_model=List[schemas.LivestockProductionRead])
def get_all_productions(db: Session = Depends(get_db)):
    """
    Get all livestock production records.
    """
    return services.get_all_productions(db)


# -----------------------------
# FEEDING
# -----------------------------

@router.post("/feeding/", response_model=schemas.LivestockFeedingRead)
def create_feeding(feeding: schemas.LivestockFeedingCreate, db: Session = Depends(get_db)):
    """
    Record feeding for a livestock.
    """
    return services.create_feeding(db, feeding)


@router.get("/feeding/", response_model=List[schemas.LivestockFeedingRead])
def get_all_feeding(db: Session = Depends(get_db)):
    """
    Get all feeding records.
    """
    return services.get_all_feeding(db)


# -----------------------------
# ACTIVITIES
# -----------------------------

@router.post("/activities/", response_model=schemas.LivestockActivityRead)
def create_activity(activity: schemas.LivestockActivityCreate, db: Session = Depends(get_db)):
    """
    Record a livestock activity (service, vaccination, etc.).
    """
    return services.create_activity(db, activity)


@router.get("/activities/", response_model=List[schemas.LivestockActivityRead])
def get_all_activities(db: Session = Depends(get_db)):
    """
    Get all livestock activity records.
    """
    return services.get_all_activities(db)


# -----------------------------
# EXPENSES
# -----------------------------

@router.post("/expenses/", response_model=schemas.LivestockExpenseRead)
def create_expense(expense: schemas.LivestockExpenseCreate, db: Session = Depends(get_db)):
    """
    Record a livestock-related expense.
    """
    return services.create_expense(db, expense)


@router.get("/expenses/", response_model=List[schemas.LivestockExpenseRead])
def get_all_expenses(db: Session = Depends(get_db)):
    """
    Get all livestock expenses.
    """
    return services.get_all_expenses(db)


# -----------------------------
# SALES
# -----------------------------

@router.post("/sales/", response_model=schemas.LivestockSaleRead)
def create_sale(sale: schemas.LivestockSaleCreate, db: Session = Depends(get_db)):
    """
    Record sale of livestock or livestock products.
    """
    return services.create_sale(db, sale)


@router.get("/sales/", response_model=List[schemas.LivestockSaleRead])
def get_all_sales(db: Session = Depends(get_db)):
    """
    Get all livestock sales records.
    """
    return services.get_all_sales(db)
