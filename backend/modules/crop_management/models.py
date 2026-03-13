#backend/modules/crop_management/models.py
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    ForeignKey, Text
)
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import JSON

from backend.modules.farms.models import Farm, Block


# ============================================================
# CROPS
# ============================================================

class Crop(Base):
    __tablename__ = "crops"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    name = Column(String(255), nullable=False)
    variety = Column(String(255))
    planting_date = Column(Date, default=date.today)
    season_start = Column(Date)
    season_end = Column(Date)
    status = Column(String(255), default="Active")

    farm = relationship("Farm")
    block = relationship("Block")

    nursery_activities = relationship("NurseryActivity", back_populates="crop", cascade="all, delete-orphan")
    activities = relationship("CropActivity", back_populates="crop", cascade="all, delete-orphan")
    fertilizer_applications = relationship("FertilizerApplication", back_populates="crop", cascade="all, delete-orphan")
    chemical_applications = relationship("ChemicalApplication", back_populates="crop", cascade="all, delete-orphan")
    irrigation_activities = relationship("Irrigation", back_populates="crop", cascade="all, delete-orphan")
    weeding_activities = relationship("Weeding", back_populates="crop", cascade="all, delete-orphan")
    scouting_activities = relationship("Scouting", back_populates="crop", cascade="all, delete-orphan")
    soil_tests = relationship("SoilTest", back_populates="crop", cascade="all, delete-orphan")
    soil_amendments = relationship("SoilAmendment", back_populates="crop", cascade="all, delete-orphan")
    crop_rotations = relationship("CropRotation", back_populates="crop", cascade="all, delete-orphan")
    harvests = relationship("CropHarvest", back_populates="crop", cascade="all, delete-orphan")
    sales = relationship("CropSale", back_populates="crop", cascade="all, delete-orphan")
    uploads = relationship("ActivityUpload", back_populates="crop", cascade="all, delete-orphan")

    # Agronomy (cross-module)
    agronomy_recommendations = relationship(
        "AgronomyRecommendation",
        back_populates="crop",
        cascade="all, delete-orphan"
    )


# ============================================================
# NURSERY ACTIVITIES
# ============================================================

class NurseryActivity(Base):
    __tablename__ = "nursery_activities"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)

    planted_date = Column(Date, nullable=False)
    germination_rate = Column(Float)
    materials_used = Column(String(255))
    tentative_transplant_date = Column(Date)
    
    crop = relationship("Crop", back_populates="nursery_activities")
    hr_work_session_id = Column(Integer, ForeignKey("hr_work_sessions.id"), nullable=True)


    

# ============================================================
# GENERAL CROP ACTIVITIES
# ============================================================

class CropActivity(Base):
    __tablename__ = "crop_activities"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    activity_type = Column(String(255), nullable=False)
    description = Column(String(255))
    date = Column(Date, default=date.today)

    hr_work_session_id = Column(Integer, ForeignKey("hr_work_sessions.id"), nullable=True)

  
   
    crop = relationship("Crop", back_populates="activities")
    block = relationship("Block")


# ============================================================
# LAND PREPARATION
# ============================================================

class LandPreparation(Base):
    __tablename__ = "land_preparations"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    date = Column(Date)
    method = Column(String(255))

    hr_work_session_id = Column(Integer, ForeignKey("hr_work_sessions.id"), nullable=True)

    crop = relationship("Crop")
    block = relationship("Block")


# ============================================================
# IRRIGATION
# ============================================================

class Irrigation(Base):
    __tablename__ = "irrigations"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    date = Column(Date)
    method = Column(String(255))
    duration_hours = Column(Float)

    hr_work_session_id = Column(Integer, ForeignKey("hr_work_sessions.id"), nullable=True)


    crop = relationship("Crop", back_populates="irrigation_activities")
    block = relationship("Block")


# ============================================================
# FERTILIZER APPLICATION (INVENTORY-DRIVEN COST)
# ============================================================

class FertilizerApplication(Base):
    __tablename__ = "fertilizer_applications"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    fertilizer_name = Column(String(255), nullable=False)
    quantity_kg = Column(Float, nullable=False)
    date = Column(Date, default=date.today)

    inventory_transaction_id = Column(
        Integer, ForeignKey("inventory_transactions.id"), nullable=True
    )
    hr_work_session_id = Column(
        Integer, ForeignKey("hr_work_sessions.id"), nullable=True
    )

    crop = relationship("Crop", back_populates="fertilizer_applications")
    block = relationship("Block")


# ============================================================
# CHEMICAL APPLICATION
# ============================================================

class ChemicalApplication(Base):
    __tablename__ = "chemical_applications"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    chemical_name = Column(String(255), nullable=False)
    quantity_ltr = Column(Float, nullable=False)
    date = Column(Date, default=date.today)

    inventory_transaction_id = Column(
        Integer, ForeignKey("inventory_transactions.id"), nullable=True
    )
    hr_work_session_id = Column(
        Integer, ForeignKey("hr_work_sessions.id"), nullable=True
    )

    crop = relationship("Crop", back_populates="chemical_applications")
    block = relationship("Block")



# ============================================================
# WEEDING ACTIVITIES
# ============================================================

class Weeding(Base):
    __tablename__ = "weedings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    date = Column(Date)
    method = Column(String(255))

    hr_work_session_id = Column(
        Integer, ForeignKey("hr_work_sessions.id"), nullable=True
    )

   
    crop = relationship("Crop", back_populates="weeding_activities")
    block = relationship("Block")


# ============================================================
# SCOUTING ACTIVITIES
# ============================================================

class Scouting(Base):
    __tablename__ = "scouting_records"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    date = Column(Date)
    pests = Column(Text)
    diseases = Column(Text)
    nutrient_deficiency = Column(Text)
    notes = Column(Text)

    hr_work_session_id = Column(
        Integer, ForeignKey("hr_work_sessions.id"), nullable=True
    )

    
    crop = relationship("Crop", back_populates="scouting_activities")
    block = relationship("Block")


# ============================================================
# SOIL TESTS
# ============================================================

class SoilTest(Base):
    __tablename__ = "soil_tests"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    date = Column(Date)
    ph = Column(Float)
    ec = Column(Float)
    n = Column(Float)
    p = Column(Float)
    k = Column(Float)
    micronutrients = Column(Text)
    lab_report = Column(String(255))

    crop = relationship("Crop", back_populates="soil_tests")
    block = relationship("Block")


# ============================================================
# SOIL AMENDMENTS
# ============================================================

class SoilAmendment(Base):
    __tablename__ = "soil_amendments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    amendment_type = Column(String(255))
    quantity = Column(Float)
    date = Column(Date)

    inventory_transaction_id = Column(
        Integer, ForeignKey("inventory_transactions.id"), nullable=True
    )

    crop = relationship("Crop", back_populates="soil_amendments")
    block = relationship("Block")


# ============================================================
# CROP ROTATIONS
# ============================================================

class CropRotation(Base):
    __tablename__ = "crop_rotations"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)

    previous_crop = Column(String(255))
    next_crop = Column(String(255))
    rotation_start = Column(Date)
    rotation_end = Column(Date)
    notes = Column(String(255))

    crop = relationship("Crop", back_populates="crop_rotations")
    block = relationship("Block")


# ============================================================
# HARVESTS
# ============================================================

class CropHarvest(Base):
    __tablename__ = "crop_harvests"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    harvest_date = Column(Date)
    field_weight = Column(Float)
    final_weight = Column(Float)
    moisture_content = Column(Float)
    grade_a = Column(Float)
    grade_b = Column(Float)
    grade_c = Column(Float)
    rejects = Column(Float)

    hr_work_session_id = Column(
        Integer, ForeignKey("hr_work_sessions.id"), nullable=True
    )

   
    crop = relationship("Crop", back_populates="harvests")
    block = relationship("Block")


# ============================================================
# SALES
# ============================================================

class CropSale(Base):
    __tablename__ = "crop_sales"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    sale_date = Column(Date)
    quantity_sold = Column(Float)
    grade_a = Column(Float)
    grade_b = Column(Float)
    grade_c = Column(Float)
    rejects_returned = Column(Float)
    price_per_unit = Column(Float)
    buyer = Column(String(255))
    income = Column(Float)

    crop = relationship("Crop", back_populates="sales")
    block = relationship("Block")


# ============================================================
# ACTIVITY UPLOADS
# ============================================================

class ActivityUpload(Base):
    __tablename__ = "activity_uploads"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)

    activity_type = Column(String(255), nullable=False)
    activity_id = Column(Integer, nullable=False)

    file_path = Column(String(255), nullable=False)
    file_type = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)

    crop = relationship("Crop", back_populates="uploads")

