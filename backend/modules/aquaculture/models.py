# backend/modules/aquaculture/models.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.core.database import Base
from datetime import date
from sqlalchemy import JSON

# ============================
# 🐟 Aquaculture / Pond
# ============================
class Aquaculture(Base):
    __tablename__ = "aquaculture"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    pond_name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    pond_size = Column(Float, nullable=True)
    stock_quantity = Column(Integer, nullable=True)
    average_weight = Column(Float, default=0.0)
    date_stocked = Column(Date, default=date.today)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    feed_type = Column(String, nullable=True)
    feed_cost = Column(Float, nullable=True)
    water_quality_status = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    farm = relationship("Farm")

    # Relationships
    feedings = relationship(
        "AquacultureFeeding",
        back_populates="pond",
        cascade="all, delete-orphan"
    )

    water_records = relationship(
        "AquacultureWaterQuality",
        back_populates="pond",
        cascade="all, delete-orphan"
    )

    harvests = relationship(
        "AquacultureHarvest",
        back_populates="pond",
        cascade="all, delete-orphan"
    )

    activities = relationship(
        "AquacultureActivity",
        back_populates="pond",
        cascade="all, delete-orphan"
    )

    productions = relationship(
        "AquacultureProduction",
        back_populates="pond",
        cascade="all, delete-orphan"
    )

    # 👉 HEALTH IS HANDLED ENTIRELY BY VETERINARY MODULE
    # Remove conflict: AquacultureHealth does NOT live in this module
    health_records = relationship(
        "backend.modules.veterinary.models.AquacultureHealth",
        back_populates="pond",
        primaryjoin="Aquaculture.id == backend.modules.veterinary.models.AquacultureHealth.pond_id",
        viewonly=True
    )


# ============================
# 🥣 Feedings
# ============================
class AquacultureFeeding(Base):
    __tablename__ = "aquaculture_feedings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, ForeignKey("aquaculture.id"))
    date = Column(Date, default=date.today)
    feed_quantity = Column(Float, nullable=False)
    feed_type = Column(String, nullable=True)
    remarks = Column(Text, nullable=True)
    consumable_id = Column(Integer, nullable=True)

    pond = relationship("Aquaculture", back_populates="feedings")


# ============================
# 💧 Water Quality
# ============================
class AquacultureWaterQuality(Base):
    __tablename__ = "aquaculture_water_quality"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, ForeignKey("aquaculture.id"))
    date = Column(Date, default=date.today)
    temperature = Column(Float, nullable=True)
    ph_level = Column(Float, nullable=True)
    dissolved_oxygen = Column(Float, nullable=True)
    ammonia = Column(Float, nullable=True)
    turbidity = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    pond = relationship("Aquaculture", back_populates="water_records")


# ============================
# 🐟 Harvest
# ============================
class AquacultureHarvest(Base):
    __tablename__ = "aquaculture_harvests"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, ForeignKey("aquaculture.id"))
    date = Column(Date, default=date.today)
    total_weight = Column(Float, nullable=False)
    average_weight = Column(Float, nullable=True)
    mortality = Column(Integer, nullable=True)
    remarks = Column(Text, nullable=True)

    pond = relationship("Aquaculture", back_populates="harvests")


# ============================
# ⚙️ Activities
# ============================
class AquacultureActivity(Base):
    __tablename__ = "aquaculture_activities"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, ForeignKey("aquaculture.id"))
    activity_type = Column(String, nullable=False)
    date = Column(Date, default=date.today)
    description = Column(Text, nullable=True)
    performed_by = Column(String, nullable=True)
    cost = Column(Float, default=0.0)
    consumable_id = Column(Integer, nullable=True)

    pond = relationship("Aquaculture", back_populates="activities")


# ============================
# 📦 Production
# ============================
class AquacultureProduction(Base):
    __tablename__ = "aquaculture_productions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, ForeignKey("aquaculture.id"))
    production_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, default=0.0)
    total_value = Column(Float, default=0.0)
    date = Column(Date, default=date.today)

    pond = relationship("Aquaculture", back_populates="productions")
