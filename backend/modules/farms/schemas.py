# backend/modules/farms/schemas.py

# backend/modules/farms/schemas.py

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

# ============================================================
# ENUMS
# ============================================================

class FarmTypeEnum(str, Enum):
    crop = "crop"
    livestock = "livestock"
    poultry = "poultry"
    aquaculture = "aquaculture"
    mixed = "mixed"


class FarmRoleEnum(str, Enum):
    owner = "owner"
    manager = "manager"
    worker = "worker"
    vet = "vet"
    agronomist = "agronomist"
    accountant = "accountant"


class SizeUnit(str, Enum):
    ha = "ha"
    ac = "ac"


class ScaleEnum(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


# ============================================================
# SIZE / AREA MODEL
# ============================================================

class Size(BaseModel):
    value: float = Field(..., description="Numeric area value")
    unit: SizeUnit = Field(..., description="Unit of area (ha or ac)")


# ============================================================
# FARM SCHEMAS
# ============================================================

class FarmBase(BaseModel):
    name: str
    location: Optional[str] = None
    farm_type: Optional[FarmTypeEnum] = None
    active_modules: List[str] = Field(default_factory=list)
    scale: ScaleEnum = ScaleEnum.small


class FarmCreate(BaseModel):
    name: str
    location: str
    farm_type: FarmTypeEnum = FarmTypeEnum.mixed
    size: Optional[Size] = None
    scale: ScaleEnum = ScaleEnum.small
    active_modules: Optional[List[str]] = None


class FarmUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    farm_type: Optional[FarmTypeEnum] = None
    active_modules: Optional[List[str]] = None
    size: Optional[Size] = None
    scale: Optional[ScaleEnum] = None


class FarmRead(FarmBase):
    id: int
    owner_id: int
    size: Optional[Size] = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# FARM MEMBER SCHEMAS
# ============================================================

class FarmMemberAssign(BaseModel):
    user_id: int
    role: FarmRoleEnum


class FarmMemberRead(BaseModel):
    id: int
    user_id: int
    role: FarmRoleEnum
    farm_id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# STRUCTURE SCHEMAS
# ============================================================

# ---------------- BLOCK ----------------

class BlockBase(BaseModel):
    name: str
    area: Size
    utilized_area: Optional[Size] = None
    in_production_fraction: Optional[float] = None


class BlockCreate(BlockBase):
    pass


class BlockRead(BlockBase):
    id: int
    farm_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------- GREENHOUSE ----------------

class GreenhouseBase(BaseModel):
    name: str
    area: Size
    utilized_area: Optional[Size] = None
    in_production_fraction: Optional[float] = None


class GreenhouseCreate(GreenhouseBase):
    pass


class GreenhouseRead(GreenhouseBase):
    id: int
    farm_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------- BARN ----------------

class BarnBase(BaseModel):
    name: str
    capacity: int


class BarnCreate(BarnBase):
    pass


class BarnRead(BarnBase):
    id: int
    farm_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------- COOP ----------------

class CoopBase(BaseModel):
    name: str
    capacity: int


class CoopCreate(CoopBase):
    pass


class CoopRead(CoopBase):
    id: int
    farm_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------- POND ----------------

class PondBase(BaseModel):
    name: str
    size: Size
    utilized_area: Optional[Size] = None
    in_production_fraction: Optional[float] = None


class PondCreate(PondBase):
    pass


class PondRead(PondBase):
    id: int
    farm_id: int

    model_config = ConfigDict(from_attributes=True)
