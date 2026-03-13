# backend/modules/livestock/models.py
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    ForeignKey, Enum, Boolean, Text
)
from sqlalchemy.orm import relationship
import enum
from backend.core.database import Base
from sqlalchemy import JSON

# -----------------------------
# ENUMS
# -----------------------------
class LivestockTypeEnum(str, enum.Enum):
    CATTLE = "Cattle"
    SHEEP = "Sheep"
    GOAT = "Goat"
    PIG = "Pig"
    OTHER = "Other"


class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"


class ActivityTypeEnum(str, enum.Enum):
    SERVICE = "service"
    CONSUMABLE = "consumable"


class ActivityCategoryEnum(str, enum.Enum):
    HEALTH = "health"
    BREEDING = "breeding"
    MANAGEMENT = "management"


class FeedingMethodEnum(str, enum.Enum):
    PASTURE = "pasture"
    STALL = "stall"
    MIXED = "mixed"


class ProductionTypeEnum(str, enum.Enum):
    MILK = "Milk"
    MEAT = "Meat"
    MANURE = "Manure"
    GENERIC = "Generic"


class LivestockStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    SLAUGHTERED = "slaughtered"
    DECEASED = "deceased"


# -----------------------------
# LIVESTOCK MASTER RECORD
# -----------------------------
class Livestock(Base):
    __tablename__ = "livestock"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tag_number = Column(String, unique=True, nullable=True)

    type = Column(Enum(LivestockTypeEnum), nullable=False)
    breed = Column(String, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=False)

    date_of_birth = Column(Date, nullable=True)
    purchase_date = Column(Date, nullable=True)
    purchase_price = Column(Float, default=0.0)

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    barn_id = Column(Integer, ForeignKey("barns.id"), nullable=True)
    group_id = Column(Integer, ForeignKey("livestock_groups.id"), nullable=True)

    status = Column(
        Enum(LivestockStatusEnum),
        default=LivestockStatusEnum.ACTIVE,
        nullable=False
    )

    remarks = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    feedings = relationship("LivestockFeeding", back_populates="livestock")
    activities = relationship("LivestockActivity", back_populates="livestock")
    productions = relationship("LivestockProduction", back_populates="livestock")
    sales = relationship("LivestockSale", back_populates="livestock")
    expenses = relationship("LivestockExpense", back_populates="livestock")
    weight_records = relationship("LivestockWeightRecord", back_populates="livestock")

    # ✅ FIXED BREEDING RELATIONSHIPS
    breedings_as_dam = relationship(
        "LivestockBreeding",
        foreign_keys="LivestockBreeding.dam_id",
        back_populates="dam",
        cascade="all, delete-orphan"
    )

    breedings_as_sire = relationship(
        "LivestockBreeding",
        foreign_keys="LivestockBreeding.sire_id",
        back_populates="sire",
        cascade="all, delete-orphan"
    )

    group = relationship("LivestockGroup", back_populates="livestock_members")


# -----------------------------
# LIVESTOCK GROUP / HERD
# -----------------------------
class LivestockGroup(Base):
    __tablename__ = "livestock_groups"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    description = Column(Text, nullable=True)

    livestock_members = relationship("Livestock", back_populates="group")
    feedings = relationship("LivestockFeeding", back_populates="group")


# -----------------------------
# WEIGHT TRACKING
# -----------------------------
class LivestockWeightRecord(Base):
    __tablename__ = "livestock_weight_records"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    livestock_id = Column(Integer, ForeignKey("livestock.id"), nullable=False)
    weight = Column(Float, nullable=False)
    date_recorded = Column(Date, default=date.today)

    livestock = relationship("Livestock", back_populates="weight_records")


# -----------------------------
# FEEDING (INDIVIDUAL OR GROUP)
# -----------------------------
class LivestockFeeding(Base):
    __tablename__ = "livestock_feedings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    livestock_id = Column(Integer, ForeignKey("livestock.id"), nullable=True)
    group_id = Column(Integer, ForeignKey("livestock_groups.id"), nullable=True)

    feed_item_id = Column(Integer, ForeignKey("store_items.id"), nullable=False)
    feeding_method = Column(Enum(FeedingMethodEnum), nullable=False)
    quantity = Column(Float, nullable=False)

    inventory_transaction_id = Column(
        Integer, ForeignKey("inventory_transactions.id"), nullable=False
    )
    hr_work_session_id = Column(
        Integer, ForeignKey("hr_work_sessions.id"), nullable=True
    )

    feeding_date = Column(Date, default=date.today)
    remarks = Column(Text, nullable=True)

    livestock = relationship("Livestock", back_populates="feedings")
    group = relationship("LivestockGroup", back_populates="feedings")
    feed_item = relationship("StoreItem")


# -----------------------------
# ACTIVITIES
# -----------------------------
class LivestockActivity(Base):
    __tablename__ = "livestock_activities"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    livestock_id = Column(Integer, ForeignKey("livestock.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    activity_type = Column(Enum(ActivityTypeEnum), nullable=False)
    activity_category = Column(Enum(ActivityCategoryEnum), nullable=False)

    performed_by = Column(String, nullable=True)

    store_item_id = Column(Integer, ForeignKey("store_items.id"), nullable=True)
    quantity_used = Column(Float, nullable=True)

    inventory_transaction_id = Column(
        Integer, ForeignKey("inventory_transactions.id"), nullable=False
    )
    hr_work_session_id = Column(
        Integer, ForeignKey("hr_work_sessions.id"), nullable=True
    )


    date_performed = Column(Date, default=date.today)

    livestock = relationship("Livestock", back_populates="activities")
    store_item = relationship("StoreItem")


# -----------------------------
# PRODUCTION
# -----------------------------
class LivestockProduction(Base):
    __tablename__ = "livestock_productions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    livestock_id = Column(Integer, ForeignKey("livestock.id"), nullable=False)

    production_type = Column(Enum(ProductionTypeEnum), nullable=False)
    quantity = Column(Float, nullable=False)

    fat_content = Column(Float, nullable=True)
    carcass_weight = Column(Float, nullable=True)

    date_recorded = Column(Date, default=date.today)
    remarks = Column(Text, nullable=True)

    livestock = relationship("Livestock", back_populates="productions")
    sale = relationship("LivestockSale", back_populates="production", uselist=False)


# -----------------------------
# SALES
# -----------------------------
class LivestockSale(Base):
    __tablename__ = "livestock_sales"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    livestock_id = Column(Integer, ForeignKey("livestock.id"), nullable=False)
    production_id = Column(Integer, ForeignKey("livestock_productions.id"), nullable=True)

    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_sale = Column(Float, nullable=False)

    buyer_name = Column(String, nullable=True)
    payment_status = Column(String, default="paid")
    date = Column(Date, default=date.today)

    livestock = relationship("Livestock", back_populates="sales")
    production = relationship("LivestockProduction", back_populates="sale")


# -----------------------------
# BREEDING / REPRODUCTION
# -----------------------------
class LivestockBreeding(Base):
    __tablename__ = "livestock_breeding"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    dam_id = Column(Integer, ForeignKey("livestock.id"), nullable=False)
    sire_id = Column(Integer, ForeignKey("livestock.id"), nullable=True)

    service_date = Column(Date, nullable=False)
    method = Column(String, nullable=True)

    expected_birth_date = Column(Date, nullable=True)
    actual_birth_date = Column(Date, nullable=True)

    offspring_count = Column(Integer, default=0)
    remarks = Column(Text, nullable=True)

    dam = relationship(
        "Livestock",
        foreign_keys=[dam_id],
        back_populates="breedings_as_dam"
    )

    sire = relationship(
        "Livestock",
        foreign_keys=[sire_id],
        back_populates="breedings_as_sire"
    )


# -----------------------------
# EXPENSES
# -----------------------------
class LivestockExpense(Base):
    __tablename__ = "livestock_expenses"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    livestock_id = Column(Integer, ForeignKey("livestock.id"), nullable=False)

    finance_base_id = Column(
        Integer, ForeignKey("finance_base.id"), nullable=False
    )

    category = Column(String, default="Livestock")
    sub_category = Column(String, nullable=True)

    date = Column(Date, default=date.today)

    livestock = relationship("Livestock", back_populates="expenses")


