#backend/modules/farms/services.py
# backend/modules/farms/services.py

from sqlalchemy.orm import Session
from . import models
from backend.modules.users.models import User
from backend.modules.audit import services as audit_services
from backend.core.module_registry import resolve_modules

# ============================================================
# PRODUCTION MODULES
# ============================================================

ALLOWED_PRODUCTION_MODULES = {
    "crop",
    "livestock",
    "poultry",
    "aquaculture",
}

# ============================================================
# ROLE PERMISSIONS
# ============================================================

ROLE_PERMISSIONS = {
    "owner": {"*"},
    "manager": {"read_farm", "manage_structures", "list_members"},
    "worker": {"read_farm"},
    "vet": {"read_farm", "read_livestock"},
    "agronomist": {"read_farm", "manage_crop"},
    "accountant": {"read_farm", "read_finance"},
}

# ============================================================
# AREA UTILITIES (JSON SAFE)
# ============================================================

HECTARES_TO_ACRES = 2.47105


def normalize_area(area_dict):
    """
    Always store area internally as:
    {"value": float_in_hectares, "unit": "ha"}
    """
    if not area_dict:
        return {"value": 0.0, "unit": "ha"}

    value = float(area_dict.get("value", 0))
    unit = area_dict.get("unit", "ha")

    if unit == "ac":
        value *= 0.404686
    elif unit != "ha":
        raise ValueError(f"Unsupported area unit: {unit}")

    return {"value": value, "unit": "ha"}


def to_size(size_json, unit="ha"):
    """
    Convert stored JSON size to requested unit.
    """
    if not size_json:
        return {"value": 0.0, "unit": unit}

    value = float(size_json.get("value", 0))

    if unit == "ac":
        return {"value": round(value * HECTARES_TO_ACRES, 4), "unit": "ac"}

    return {"value": round(value, 4), "unit": "ha"}


# ============================================================
# PERMISSIONS
# ============================================================

def get_user_farm_role(db: Session, farm_id: int, user_id: int):
    member = (
        db.query(models.FarmMember)
        .filter(
            models.FarmMember.farm_id == farm_id,
            models.FarmMember.user_id == user_id,
        )
        .first()
    )
    return member.role if member else None


def require_farm_permission(db: Session, farm: models.Farm, user_id: int, permission: str):
    if farm.owner_id == user_id:
        return

    role = get_user_farm_role(db, farm.id, user_id)
    if not role:
        raise PermissionError("User is not a farm member")

    allowed = ROLE_PERMISSIONS.get(role.value, set())

    if "*" in allowed or permission in allowed:
        return

    raise PermissionError("Insufficient permissions")


# ============================================================
# FARM CRUD
# ============================================================

def create_farm(db: Session, farm_data: dict, actor_id: int):
    farm_type = farm_data.get("farm_type")
    selected_modules = farm_data.get("active_modules") or []

    if not selected_modules:
        if farm_type and farm_type != models.FarmTypeEnum.mixed:
            selected_modules = [farm_type.value]
        else:
            raise ValueError("At least one production module must be selected")

    invalid = set(selected_modules) - ALLOWED_PRODUCTION_MODULES
    if invalid:
        raise ValueError(f"Invalid production modules: {invalid}")

    farm_data["active_modules"] = resolve_modules(selected_modules)

    if "size" in farm_data:
        farm_data["size"] = normalize_area(farm_data["size"])

    # Create farm record
    farm = models.Farm(**farm_data)
    db.add(farm)
    db.commit()
    db.refresh(farm)

    audit_services.log_action(
        db,
        user_id=actor_id,
        action="create",
        resource="farm",
        resource_id=farm.id,
    )

    # ------------------------------
    # AUTO-CREATE DEFAULT STRUCTURES
    # ------------------------------
    default_structures = {
        "small": {"barns": 1, "coops": 1, "ponds": 0},
        "medium": {"barns": 2, "coops": 2, "ponds": 1},
        "large": {"barns": 5, "coops": 5, "ponds": 3},
    }

    counts = default_structures.get(farm.scale.value if hasattr(farm.scale, "value") else farm.scale,
                                    {"barns": 1, "coops": 1, "ponds": 0})

    for i in range(counts["barns"]):
        create_barn(db, {"name": f"Barn {i+1}", "capacity": 0, "farm_id": farm.id}, actor_id)
    for i in range(counts["coops"]):
        create_coop(db, {"name": f"Coop {i+1}", "capacity": 0, "farm_id": farm.id}, actor_id)
    for i in range(counts["ponds"]):
        create_pond(db, {"name": f"Pond {i+1}", "size": {"value": 0, "unit": "ha"}, "farm_id": farm.id}, actor_id)

    return farm

def update_farm(db: Session, farm_id: int, farm_data: dict, actor_id: int):
    farm = db.query(models.Farm).filter(models.Farm.id == farm_id).first()
    if not farm:
        return None

    # Handle active modules
    if "active_modules" in farm_data:
        selected_modules = farm_data["active_modules"] or []
        if not selected_modules:
            raise ValueError("At least one production module must be selected")

        invalid = set(selected_modules) - ALLOWED_PRODUCTION_MODULES
        if invalid:
            raise ValueError(f"Invalid production modules: {invalid}")

        farm.active_modules = resolve_modules(selected_modules)

    # Handle area
    if "size" in farm_data:
        farm.size = normalize_area(farm_data["size"])

    # Handle scale change and auto-adjust structures
    if "scale" in farm_data and farm_data["scale"] != farm.scale:
        old_scale = farm.scale
        new_scale = farm_data["scale"]
        farm.scale = new_scale

        # Default structures mapping
        default_structures = {
            "small": {"barns": 1, "coops": 1, "ponds": 0},
            "medium": {"barns": 2, "coops": 2, "ponds": 1},
            "large": {"barns": 5, "coops": 5, "ponds": 3},
        }

        old_counts = default_structures.get(old_scale, {"barns": 1, "coops": 1, "ponds": 0})
        new_counts = default_structures.get(new_scale, {"barns": 1, "coops": 1, "ponds": 0})

        # Adjust barns
        existing_barns = db.query(models.Barn).filter(models.Barn.farm_id == farm.id).all()
        if len(existing_barns) < new_counts["barns"]:
            for i in range(len(existing_barns), new_counts["barns"]):
                create_barn(db, {"name": f"Barn {i+1}", "capacity": 0, "farm_id": farm.id}, actor_id)
        elif len(existing_barns) > new_counts["barns"]:
            for barn in existing_barns[new_counts["barns"]:]:
                db.delete(barn)

        # Adjust coops
        existing_coops = db.query(models.Coop).filter(models.Coop.farm_id == farm.id).all()
        if len(existing_coops) < new_counts["coops"]:
            for i in range(len(existing_coops), new_counts["coops"]):
                create_coop(db, {"name": f"Coop {i+1}", "capacity": 0, "farm_id": farm.id}, actor_id)
        elif len(existing_coops) > new_counts["coops"]:
            for coop in existing_coops[new_counts["coops"]:]:
                db.delete(coop)

        # Adjust ponds
        existing_ponds = db.query(models.Pond).filter(models.Pond.farm_id == farm.id).all()
        if len(existing_ponds) < new_counts["ponds"]:
            for i in range(len(existing_ponds), new_counts["ponds"]):
                create_pond(db, {"name": f"Pond {i+1}", "size": {"value": 0, "unit": "ha"}, "farm_id": farm.id}, actor_id)
        elif len(existing_ponds) > new_counts["ponds"]:
            for pond in existing_ponds[new_counts["ponds"]:]:
                db.delete(pond)

    # Update other fields
    for key, value in farm_data.items():
        if key not in ("active_modules", "size", "scale"):
            setattr(farm, key, value)

    db.commit()
    db.refresh(farm)

    audit_services.log_action(
        db,
        user_id=actor_id,
        action="update",
        resource="farm",
        resource_id=farm.id,
    )

    return farm

def delete_farm(db: Session, farm_id: int, actor_id: int):
    farm = db.query(models.Farm).filter(models.Farm.id == farm_id).first()
    if not farm:
        return None

    db.delete(farm)
    db.commit()

    audit_services.log_action(
        db,
        user_id=actor_id,
        action="delete",
        resource="farm",
        resource_id=farm_id,
    )

    return farm


def list_user_farms(db: Session, user_id: int):
    owned = db.query(models.Farm).filter(models.Farm.owner_id == user_id).all()

    member_of = (
        db.query(models.Farm)
        .join(models.FarmMember)
        .filter(models.FarmMember.user_id == user_id)
        .all()
    )

    farms = owned + [f for f in member_of if f not in owned]

    return farms

# ============================================================
# STRUCTURES
# ============================================================

def list_farm_blocks(db: Session, farm_id: int, size_unit: str = "ha"):
    blocks = db.query(models.Block).filter(models.Block.farm_id == farm_id).all()
    result = []
    for b in blocks:
        b_dict = b.__dict__.copy()
        b_dict["area"] = to_size(b_dict.get("area"), unit=size_unit)
        if b_dict.get("utilized_area"):
            b_dict["utilized_area"] = to_size(b_dict.get("utilized_area"), unit=size_unit)
        result.append(b_dict)
    return result



def list_farm_greenhouses(db: Session, farm_id: int, size_unit: str = "ha"):
    greenhouses = db.query(models.Greenhouse).filter(models.Greenhouse.farm_id == farm_id).all()
    result = []
    for g in greenhouses:
        g_dict = g.__dict__.copy()
        g_dict["area"] = to_size(g_dict.get("area"), unit=size_unit)
        if g_dict.get("utilized_area"):
            g_dict["utilized_area"] = to_size(g_dict.get("utilized_area"), unit=size_unit)
        result.append(g_dict)
    return result


def list_farm_barns(db: Session, farm_id: int):
    barns = db.query(models.Barn).filter(models.Barn.farm_id == farm_id).all()
    result = [b.__dict__.copy() for b in barns]
    return result


def list_farm_coops(db: Session, farm_id: int):
    coops = db.query(models.Coop).filter(models.Coop.farm_id == farm_id).all()
    result = [c.__dict__.copy() for c in coops]
    return result


def list_farm_ponds(db: Session, farm_id: int, size_unit: str = "ha"):
    ponds = db.query(models.Pond).filter(models.Pond.farm_id == farm_id).all()
    result = []
    for p in ponds:
        p_dict = p.__dict__.copy()
        p_dict["size"] = to_size(p_dict.get("size"), unit=size_unit)
        if p_dict.get("utilized_area"):
            p_dict["utilized_area"] = to_size(p_dict.get("utilized_area"), unit=size_unit)
        result.append(p_dict)
    return result



# ============================================================
# FARM DETAILS
# ============================================================

def get_farm_details(db: Session, farm_id: int, unit: str = "ha"):
    """
    Fetch a farm with all its structures, members, and normalized areas.
    Returns a JSON-ready dictionary.
    """

    # Fetch the farm
    farm = db.query(models.Farm).filter(models.Farm.id == farm_id).first()
    if not farm:
        return None

    # Fetch members
    members = (
        db.query(models.FarmMember)
        .filter(models.FarmMember.farm_id == farm_id)
        .all()
    )
    member_list = [
        {
            "id": m.id,
            "user_id": m.user_id,
            "role": m.role.value,
        }
        for m in members
    ]

    # Fetch structures
    blocks = db.query(models.Block).filter(models.Block.farm_id == farm_id).all()
    greenhouses = db.query(models.Greenhouse).filter(models.Greenhouse.farm_id == farm_id).all()
    barns = db.query(models.Barn).filter(models.Barn.farm_id == farm_id).all()
    coops = db.query(models.Coop).filter(models.Coop.farm_id == farm_id).all()
    ponds = db.query(models.Pond).filter(models.Pond.farm_id == farm_id).all()

    # Helper to serialize structures
    def serialize_structure(obj, area_field="area", utilized_field="utilized_area"):
        data = obj.__dict__.copy()
        # Remove SQLAlchemy internal keys
        data.pop("_sa_instance_state", None)
        # Normalize areas
        if hasattr(obj, area_field):
            data[area_field] = to_size(getattr(obj, area_field), unit)
        if hasattr(obj, utilized_field):
            ua = getattr(obj, utilized_field)
            if ua:
                data[utilized_field] = to_size(ua, unit)
        return data

    return {
        "id": farm.id,
        "name": farm.name,
        "location": farm.location,
        "farm_type": farm.farm_type.value if farm.farm_type else None,
        "owner_id": farm.owner_id,
        "active_modules": farm.active_modules,
        "size": to_size(farm.size, unit) if farm.size else {"value": 0, "unit": unit},
        "members": member_list,
        "blocks": [serialize_structure(b) for b in blocks],
        "greenhouses": [serialize_structure(g) for g in greenhouses],
        "barns": [serialize_structure(b, area_field=None, utilized_field=None) for b in barns],
        "coops": [serialize_structure(c, area_field=None, utilized_field=None) for c in coops],
        "ponds": [serialize_structure(p, area_field="size") for p in ponds],
    }


def update_structure(db: Session, obj, payload: dict, actor_id: int):
    for key, value in payload.items():
        setattr(obj, key, value)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_structure(db: Session, obj, actor_id: int):
    db.delete(obj)
    db.commit()
    return True
