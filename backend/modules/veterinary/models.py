#backend/modules/veterinary/models.py

from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import JSON
import enum

# ============================================================
# ENUM for group_type
# ============================================================
class GroupTypeEnum(str, enum.Enum):
    POULTRY = "poultry"
    LIVESTOCK = "livestock"
    AQUACULTURE = "aquaculture"

# ============================================================
# ANIMAL GROUP
# ============================================================
class AnimalGroup(Base):
    __tablename__ = "animal_groups"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    group_type = Column(Enum(GroupTypeEnum), nullable=False)
    quantity = Column(Integer, default=0)
    date_added = Column(Date, default=lambda: date.today())
    notes = Column(Text, nullable=True)

    poultry_health = relationship(
        "PoultryHealth", back_populates="animal_group", cascade="all, delete-orphan"
    )
    aquaculture_health = relationship(
        "AquacultureHealth", back_populates="animal_group", cascade="all, delete-orphan"
    )
    livestock_health = relationship(
        "LivestockHealth", back_populates="animal_group", cascade="all, delete-orphan"
    )
    recommendations = relationship(
        "VeterinaryRecommendation", back_populates="animal_group"
    )

# ============================================================
# POULTRY HEALTH
# ============================================================
class PoultryHealth(Base):
    __tablename__ = "poultry_health"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    animal_group_id = Column(Integer, ForeignKey("animal_groups.id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("poultry_batches.id"), nullable=True)
    date_checked = Column(Date, default=lambda: date.today())
    symptoms = Column(Text, nullable=True)
    mortality = Column(Integer, default=0)
    disease_detected = Column(String, nullable=True)
    treatment_given = Column(Text, nullable=True)
    health_status = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    animal_group = relationship("AnimalGroup", back_populates="poultry_health")
    batch = relationship("PoultryBatch", back_populates="health_records")

# ============================================================
# AQUACULTURE HEALTH
# ============================================================
class AquacultureHealth(Base):
    __tablename__ = "aquaculture_health"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    pond_id = Column(Integer, ForeignKey("aquaculture.id"), nullable=False)
    animal_group_id = Column(Integer, ForeignKey("animal_groups.id"), nullable=False)
    date_checked = Column(Date, default=lambda: date.today())
    symptoms = Column(Text, nullable=True)
    mortality = Column(Integer, default=0)
    disease_detected = Column(String, nullable=True)
    treatment_given = Column(Text, nullable=True)
    water_quality_status = Column(String, nullable=True)
    health_status = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    pond = relationship("Aquaculture", back_populates="health_records")
    animal_group = relationship("AnimalGroup", back_populates="aquaculture_health")

# ============================================================
# LIVESTOCK HEALTH
# ============================================================
class LivestockHealth(Base):
    __tablename__ = "livestock_health"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    livestock_id = Column(Integer, ForeignKey("livestock.id"), nullable=False)
    animal_group_id = Column(Integer, ForeignKey("animal_groups.id"), nullable=False)
    date_checked = Column(Date, default=lambda: date.today())
    symptoms = Column(Text, nullable=True)
    disease_detected = Column(String, nullable=True)
    treatment_given = Column(Text, nullable=True)
    health_status = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    livestock = relationship("Livestock")
    animal_group = relationship("AnimalGroup", back_populates="livestock_health")

# ============================================================
# VETERINARY RECOMMENDATION
# ============================================================
class VeterinaryRecommendation(Base):
    __tablename__ = "veterinary_recommendations"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    livestock_health_id = Column(Integer, ForeignKey("livestock_health.id"), nullable=True)
    poultry_health_id = Column(Integer, ForeignKey("poultry_health.id"), nullable=True)
    aquaculture_health_id = Column(Integer, ForeignKey("aquaculture_health.id"), nullable=True)
    animal_group_id = Column(Integer, ForeignKey("animal_groups.id"), nullable=True)
    recommendation_text = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=True)
    date_given = Column(Date, default=lambda: date.today())

    livestock_health = relationship("LivestockHealth")
    poultry_health = relationship("PoultryHealth")
    aquaculture_health = relationship("AquacultureHealth")
    animal_group = relationship("AnimalGroup", back_populates="recommendations")

# ============================================================
# VETERINARY FILE UPLOADS
# ============================================================
class VeterinaryUpload(Base):
    __tablename__ = "veterinary_uploads"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("veterinary_recommendations.id"), nullable=True)
    livestock_health_id = Column(Integer, ForeignKey("livestock_health.id"), nullable=True)
    poultry_health_id = Column(Integer, ForeignKey("poultry_health.id"), nullable=True)
    aquaculture_health_id = Column(Integer, ForeignKey("aquaculture_health.id"), nullable=True)

    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date_uploaded = Column(Date, default=lambda: date.today())

    recommendation = relationship("VeterinaryRecommendation", backref="uploads")
    livestock_health = relationship("LivestockHealth", backref="uploads")
    poultry_health = relationship("PoultryHealth", backref="uploads")
    aquaculture_health = relationship("AquacultureHealth", backref="uploads")

