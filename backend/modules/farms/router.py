#backend/modules/farms/router.py
# backend/modules/farms/router.py

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from typing import List

from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.core.farm_context import get_current_farm
from backend.core.module_registry import resolve_modules

from . import models, schemas, services

router = APIRouter(tags=["Farms"])

# ============================================================
# INTERNAL HELPERS
# ============================================================

def get_farm(db: Session, farm_id: int):
    return db.query(models.Farm).filter(models.Farm.id == farm_id).first()


def get_owned_farm(db: Session, farm_id: int, user_id: int):
    farm = get_farm(db, farm_id)
    if farm and farm.owner_id == user_id:
        return farm
    return None


def require_permission(db, farm, user_id, permission: str):
    try:
        services.require_farm_permission(db, farm, user_id, permission)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# -----------------------------
# SERIALIZERS
# -----------------------------

def serialize_farm(farm, unit="ha"):
    if not farm:
        return None

    data = {
        column.name: getattr(farm, column.name)
        for column in farm.__table__.columns
    }

    if "size" in data and data["size"] is not None:
        data["size"] = services.to_size(data["size"], unit)

    return data


def serialize_structure(obj, unit="ha"):
    if not obj:
        return None

    data = {
        column.name: getattr(obj, column.name)
        for column in obj.__table__.columns
    }

    if "area" in data and data["area"] is not None:
        data["area"] = services.to_size(data["area"], unit)

    if "size" in data and data["size"] is not None:
        data["size"] = services.to_size(data["size"], unit)

    if "utilized_area" in data and data["utilized_area"] is not None:
        data["utilized_area"] = services.to_size(data["utilized_area"], unit)

    return data


def serialize_structure_list(objs, unit="ha"):
    return [serialize_structure(o, unit) for o in objs]


def create_structure_helper(factory_func, farm_id, payload, db, current_user, unit="ha"):
    farm = get_owned_farm(db, farm_id, current_user.id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    payload_dict = payload.model_dump()
    payload_dict["farm_id"] = farm_id

    obj = factory_func(
        db=db,
        data=payload_dict,
        actor_id=current_user.id,
        unit=unit,
    )

    return serialize_structure(obj, unit)

# ============================================================
# FARM MEMBERS (OWNER ONLY)
# ============================================================

@router.post("/{farm_id}/members", response_model=schemas.FarmMemberRead, status_code=status.HTTP_201_CREATED)
def add_farm_member(
    farm_id: int,
    payload: schemas.FarmMemberAssign,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farm = get_farm(db, farm_id)
    if not farm or farm.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can manage members")

    return services.add_farm_member(
        db=db,
        farm_id=farm_id,
        user_id=payload.user_id,
        role=payload.role,
        actor_id=current_user.id,
    )


@router.get("", response_model=List[schemas.FarmRead])
def list_farms(
    unit: str = Query("ha", pattern="^(ha|ac)$"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farms = services.list_user_farms(db, current_user.id)
    return [serialize_farm(f, unit) for f in farms]


@router.delete("/{farm_id}/members/{member_id}")
def remove_farm_member(
    farm_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farm = get_farm(db, farm_id)
    if not farm or farm.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can remove members")

    member = services.remove_farm_member(db, farm_id, member_id, actor_id=current_user.id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return {"detail": "Member removed successfully"}


# ============================================================
# FARM CRUD
# ============================================================

@router.post("", response_model=schemas.FarmRead, status_code=status.HTTP_201_CREATED)
def create_farm(
    payload: schemas.FarmCreate,
    unit: str = Query("ha", pattern="^(ha|ac)$"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = payload.model_dump()
    data["owner_id"] = current_user.id

    # -------------------------------
    # AUTO MODULE RESOLUTION
    # -------------------------------
    selected_modules = data.get("active_modules") or []
    data["active_modules"] = resolve_modules(selected_modules)

    farm = services.create_farm(db, data, actor_id=current_user.id)
    return serialize_farm(farm, unit)


@router.get("", response_model=List[schemas.FarmRead])
def list_farms(
    unit: str = Query("ha", pattern="^(ha|ac)$"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farms = services.list_user_farms(db, current_user.id)
    return [serialize_farm(f, unit) for f in farms]


@router.get("/{farm_id}/details")
def get_farm_details(
    farm_id: int,
    unit: str = Query("ha", pattern="^(ha|ac)$"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farm = get_farm(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    require_permission(db, farm, current_user.id, "read_farm")
    return services.get_farm_details(db, farm_id, unit)


@router.put("/{farm_id}", response_model=schemas.FarmRead)
def update_farm(
    farm_id: int,
    payload: schemas.FarmUpdate,
    unit: str = Query("ha", pattern="^(ha|ac)$"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farm = get_farm(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    require_permission(db, farm, current_user.id, "manage_farm")

    update_data = payload.model_dump(exclude_unset=True)

    if "active_modules" in update_data:
        update_data["active_modules"] = resolve_modules(update_data["active_modules"])

    updated = services.update_farm(
        db,
        farm_id,
        update_data,
        actor_id=current_user.id,
    )

    return serialize_farm(updated, unit)


@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farm = get_owned_farm(db, farm_id, current_user.id)
    if not farm:
        raise HTTPException(status_code=403, detail="Only owner can delete farm")

    services.delete_farm(db, farm_id, actor_id=current_user.id)
    return None

# ============================================================
# SINGLE FARM (CLEAN REST ENDPOINT)
# ============================================================

@router.get("/{farm_id}", response_model=schemas.FarmRead)
def get_farm_by_id(
    farm_id: int,
    unit: str = Query("ha", pattern="^(ha|ac)$"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farm = get_farm(db, farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    require_permission(db, farm, current_user.id, "read_farm")

    return serialize_farm(farm, unit)


# ============================================================
# STRUCTURE CREATION (OWNER SCOPED)
# ============================================================

@router.post("/{farm_id}/blocks", response_model=schemas.BlockRead)
def create_block(
    farm_id: int,
    payload: schemas.BlockCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    unit: str = "ha",
):
    return create_structure_helper(services.create_block, farm_id, payload, db, current_user, unit)


@router.post("/{farm_id}/greenhouses", response_model=schemas.GreenhouseRead)
def create_greenhouse(
    farm_id: int,
    payload: schemas.GreenhouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    unit: str = "ha",
):
    return create_structure_helper(services.create_greenhouse, farm_id, payload, db, current_user, unit)


@router.post("/{farm_id}/barns", response_model=schemas.BarnRead)
def create_barn(
    farm_id: int,
    payload: schemas.BarnCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_structure_helper(services.create_barn, farm_id, payload, db, current_user)


@router.post("/{farm_id}/coops", response_model=schemas.CoopRead)
def create_coop(
    farm_id: int,
    payload: schemas.CoopCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_structure_helper(services.create_coop, farm_id, payload, db, current_user)


@router.post("/{farm_id}/ponds", response_model=schemas.PondRead)
def create_pond(
    farm_id: int,
    payload: schemas.PondCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    unit: str = "ha",
):
    return create_structure_helper(services.create_pond, farm_id, payload, db, current_user, unit)

# ============================================================
# STRUCTURES SUMMARY
# ============================================================

@router.get("/{farm_id}/structures")
def get_farm_structures(
    farm_id: int,
    unit: str = Query("ha", pattern="^(ha|ac)$"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    farm = get_owned_farm(db, farm_id, current_user.id)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    return {
        "blocks": serialize_structure_list(farm.blocks, unit),
        "greenhouses": serialize_structure_list(farm.greenhouses, unit),
        "barns": serialize_structure_list(farm.barns),
        "coops": serialize_structure_list(farm.coops),
        "ponds": serialize_structure_list(farm.ponds, unit),
    }


