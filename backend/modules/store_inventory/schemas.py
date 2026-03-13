#backend/modules/store_inventory/schemas.py

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


# ------------------------------------------------------------
# HELPER: CASE-INSENSITIVE ENUM NORMALIZATION
# ------------------------------------------------------------
def normalize_enum(enum_class, value: str):
    """Convert any-case input into the correct Enum value."""
    if not isinstance(value, str):
        return value

    for enum_member in enum_class:
        if value.lower() == enum_member.value.lower():
            return enum_member

    raise ValueError(
        f"Invalid value '{value}' for enum {enum_class.__name__}. "
        f"Allowed: {[e.value for e in enum_class]}"
    )


# ------------------------------------------------------------
# ENUMS (Same as before: DO NOT CHANGE VALUES)
# ------------------------------------------------------------
class ItemCategory(str, Enum):
    SEED = "Seed"
    FERTILIZER = "Fertilizer"
    CHEMICAL = "Chemical"
    TOOL = "Tool"
    MACHINE = "Machine"
    FEED = "Feed"
    DRUG = "Drug"
    GENERAL = "General"


class ModuleType(str, Enum):
    CROP = "Crop"
    LIVESTOCK = "Livestock"
    POULTRY = "Poultry"
    AQUACULTURE = "Aquaculture"
    GENERAL = "General"


class TransactionType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"


# ------------------------------------------------------------
# STORE ITEM SCHEMAS
# ------------------------------------------------------------
class StoreItemBase(BaseModel):
    name: str
    category: ItemCategory
    module_type: ModuleType = ModuleType.GENERAL

    purchase_unit: Optional[str] = "unit"
    usage_unit: Optional[str] = "unit"
    conversion_factor: Optional[float] = 1.0

    quantity_in_stock: float = 0.0
    unit_cost: float = 0.0

    manufacturer: Optional[str] = None
    manufacture_date: Optional[date] = None
    expiry_date: Optional[date] = None
    composition: Optional[str] = None
    active_ingredients: Optional[str] = None
    intended_use: Optional[str] = None
    batch_number: Optional[str] = None
    storage_location: Optional[str] = None
    safety_precautions: Optional[str] = None
    remarks: Optional[str] = None
    product_website: Optional[str] = None

    reorder_level: float = 0.0
    max_stock_level: float = 0.0

    farm_id: Optional[int] = None
    linked_entity_id: Optional[int] = None
    crop_id: Optional[int] = None
    season_end: Optional[date] = None

    # -------------------- VALIDATORS --------------------
    @validator("category", pre=True)
    def normalize_category(cls, v):
        return normalize_enum(ItemCategory, v)

    @validator("module_type", pre=True)
    def normalize_module_type(cls, v):
        return normalize_enum(ModuleType, v)


class StoreItemCreate(StoreItemBase):
    pass


class StoreItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[ItemCategory] = None
    module_type: Optional[ModuleType] = None
    purchase_unit: Optional[str] = None
    usage_unit: Optional[str] = None
    conversion_factor: Optional[float] = None
    quantity_in_stock: Optional[float] = None
    unit_cost: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[date] = None
    expiry_date: Optional[date] = None
    composition: Optional[str] = None
    active_ingredients: Optional[str] = None
    intended_use: Optional[str] = None
    batch_number: Optional[str] = None
    storage_location: Optional[str] = None
    safety_precautions: Optional[str] = None
    remarks: Optional[str] = None
    product_website: Optional[str] = None
    reorder_level: Optional[float] = None
    max_stock_level: Optional[float] = None

    @validator("category", pre=True)
    def normalize_category(cls, v):
        if v is None:
            return v
        return normalize_enum(ItemCategory, v)

    @validator("module_type", pre=True)
    def normalize_module_type(cls, v):
        if v is None:
            return v
        return normalize_enum(ModuleType, v)


class StoreItemSchema(StoreItemBase):
    id: int
    quantity_used: float
    total_value: float
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ------------------------------------------------------------
# TRANSACTION SCHEMAS
# ------------------------------------------------------------
class InventoryTransactionBase(BaseModel):
    item_id: int
    transaction_type: TransactionType
    quantity: float
    unit_cost: Optional[float] = None

    reference: Optional[str] = None
    description: Optional[str] = None
    recorded_by: Optional[str] = None

    module_type: Optional[ModuleType] = None
    linked_entity_id: Optional[int] = None
    activity_id: Optional[int] = None

    date: Optional[datetime] = None

    @validator("module_type", pre=True)
    def normalize_module_type(cls, v):
        if v is None:
            return v
        return normalize_enum(ModuleType, v)


class InventoryTransactionCreate(InventoryTransactionBase):
    pass


class InventoryTransactionUpdate(BaseModel):
    quantity: Optional[float] = None
    unit_cost: Optional[float] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    module_type: Optional[ModuleType] = None
    linked_entity_id: Optional[int] = None
    activity_id: Optional[int] = None

    @validator("module_type", pre=True)
    def normalize_module_type(cls, v):
        if v is None:
            return v
        return normalize_enum(ModuleType, v)


class InventoryTransactionSchema(InventoryTransactionBase):
    id: int
    total_cost: Optional[float]
    is_deleted: bool
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# ------------------------------------------------------------
# EXPORT/IMPORT SUPPORT SCHEMAS
# ------------------------------------------------------------
class ImportFormat(str, Enum):
    EXCEL = "excel"
    CSV = "csv"


class InventoryImportResult(BaseModel):
    imported: int
    failed: int
    errors: List[str] = []


class TemplateType(str, Enum):
    STORE_ITEMS = "store_items"
    TRANSACTIONS = "transactions"
