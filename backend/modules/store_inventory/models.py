# backend/modules/store_inventory/models.py

from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    Enum, Text, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship, validates
from backend.core.database import Base
from sqlalchemy import JSON
import enum


# ------------------------------------------------------------
# CASE-INSENSITIVE ENUM NORMALIZER
# ------------------------------------------------------------
def normalize_enum(enum_class, value):
    """Normalize case-insensitive Enum input."""
    if value is None:
        return None

    if isinstance(value, enum_class):
        return value  # Already an enum

    if isinstance(value, str):
        for member in enum_class:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(
            f"Invalid '{value}' for enum {enum_class.__name__}. "
            f"Allowed: {[e.value for e in enum_class]}"
        )

    return value


# ------------------------------------------------------------
# Item categories
# ------------------------------------------------------------
class ItemCategory(enum.Enum):
    SEED = "Seed"
    FERTILIZER = "Fertilizer"
    CHEMICAL = "Chemical"
    TOOL = "Tool"
    MACHINE = "Machine"
    FEED = "Feed"
    DRUG = "Drug"
    GENERAL = "General"


# ------------------------------------------------------------
# Module types
# ------------------------------------------------------------
class ModuleType(enum.Enum):
    CROP = "Crop"
    LIVESTOCK = "Livestock"
    POULTRY = "Poultry"
    AQUACULTURE = "Aquaculture"
    AGRONOMY = "Agronomy"
    GENERAL = "General"


# ------------------------------------------------------------
# Transaction types
# ------------------------------------------------------------
class TransactionType(enum.Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"


# ------------------------------------------------------------
# Store Item Master
# ------------------------------------------------------------
class StoreItem(Base):
    __tablename__ = "store_items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    # Enums now accept any case input due to validators (below)
    category = Column(Enum(ItemCategory), nullable=False, default=ItemCategory.GENERAL)
    module_type = Column(Enum(ModuleType), default=ModuleType.GENERAL)

    # Units
    purchase_unit = Column(String(50), default="unit")
    usage_unit = Column(String(50), default="unit")
    conversion_factor = Column(Float, default=1.0)

    # Stock tracking
    quantity_in_stock = Column(Float, default=0.0)
    quantity_used = Column(Float, default=0.0)
    unit_cost = Column(Float, default=0.0)
    total_value = Column(Float, default=0.0)

    # Metadata
    manufacturer = Column(String(255), nullable=True)
    manufacture_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    composition = Column(Text, nullable=True)
    active_ingredients = Column(Text, nullable=True)
    intended_use = Column(Text, nullable=True)
    batch_number = Column(String(100), nullable=True)
    storage_location = Column(String(255), nullable=True)
    safety_precautions = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    product_website = Column(String(500), nullable=True)

    # Linking
    farm_id = Column(Integer, nullable=True)
    linked_entity_id = Column(Integer, nullable=True)
    crop_id = Column(Integer, nullable=True)
    season_end = Column(Date, nullable=True)

    # Alerts
    reorder_level = Column(Float, default=0.0)
    max_stock_level = Column(Float, default=0.0)

    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions = relationship("InventoryTransaction", back_populates="item")
    finance_entries = relationship("FinanceEntry", back_populates="store_item")

    # --------------------------------------------------------
    # Case-insensitive ENUM VALIDATION
    # --------------------------------------------------------
    @validates("category")
    def validate_category(self, key, value):
        return normalize_enum(ItemCategory, value)

    @validates("module_type")
    def validate_module_type(self, key, value):
        return normalize_enum(ModuleType, value)

    # --------------------------------------------------------
    # Enrichment helper
    # --------------------------------------------------------
    def enrich(self):
        info = get_product_details(self.name)
        self.manufacturer = info.get("manufacturer")
        self.active_ingredients = info.get("active_ingredient")
        self.composition = info.get("composition")
        self.product_website = info.get("product_website")
        self.safety_precautions = info.get("safety_precautions")
        return self


# ------------------------------------------------------------
# Inventory Transactions
# ------------------------------------------------------------
class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("store_items.id"), nullable=False)

    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)

    date = Column(DateTime, default=datetime.utcnow)
    reference = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    recorded_by = Column(String(255), nullable=True)

    module_type = Column(Enum(ModuleType), nullable=True)
    linked_entity_id = Column(Integer, nullable=True)
    activity_id = Column(Integer, nullable=True)

    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    item = relationship("StoreItem", back_populates="transactions")
    finance_entries = relationship("FinanceEntry", back_populates="inventory_transaction")

    # --------------------------------------------------------
    # Case-insensitive ENUM VALIDATION
    # --------------------------------------------------------
    @validates("module_type")
    def validate_module_type(self, key, value):
        return normalize_enum(ModuleType, value)


# ------------------------------------------------------------
# Finance Entries
# ------------------------------------------------------------
class FinanceEntry(Base):
    __tablename__ = "finance_entries"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    store_item_id = Column(Integer, ForeignKey("store_items.id"), nullable=True)
    transaction_id = Column(Integer, ForeignKey("inventory_transactions.id"), nullable=True)

    module_type = Column(Enum(ModuleType), nullable=True)
    linked_entity_id = Column(Integer, nullable=True)

    amount = Column(Float, nullable=False)
    entry_type = Column(String(50), nullable=False)
    date_recorded = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
    recorded_by = Column(String(255), nullable=True)

    # Relationships
    store_item = relationship("StoreItem", back_populates="finance_entries")
    inventory_transaction = relationship("InventoryTransaction", back_populates="finance_entries")

    # --------------------------------------------------------
    # Case-insensitive ENUM VALIDATION
    # --------------------------------------------------------
    @validates("module_type")
    def validate_module_type(self, key, value):
        return normalize_enum(ModuleType, value)
