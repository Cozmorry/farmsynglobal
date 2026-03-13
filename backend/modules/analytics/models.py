#backend/modules/analytics/models.py

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from backend.core.database import Base
from sqlalchemy import JSON


# ============================================================
# REGIONS (COUNTRY-AGNOSTIC ADMINISTRATIVE HIERARCHY)
# ============================================================

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)

    # ISO 3166-1 alpha-3 (KEN, NGA, USA, IND, etc.)
    country_code = Column(String(3), index=True, nullable=False)

    name = Column(String, index=True, nullable=False)

    # 0 = Country
    # 1 = State / Province / Region
    # 2 = County / District / LGA
    # 3 = Ward / Commune / Location
    level = Column(Integer, nullable=False)

    parent_id = Column(Integer, ForeignKey("regions.id"), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Self-referencing hierarchy
    parent = relationship("Region", remote_side=[id], backref="children")

    __table_args__ = (
        Index("ix_region_country_level", "country_code", "level"),
    )


# ============================================================
# REGIONAL CROP PRODUCTION STATISTICS
# ============================================================

class RegionalCropStat(Base):
    __tablename__ = "regional_crop_stats"
    __table_args__ = (
    Index(
        "uq_crop_region_period",
        "region_id",
        "crop_type",
        "season",
        "year",
        unique=True,
    ),
)


    id = Column(Integer, primary_key=True)

    region_id = Column(Integer, ForeignKey("regions.id"), index=True, nullable=False)

    crop_type = Column(String, index=True, nullable=False)
    season = Column(String, nullable=False)   # e.g. "long_rains", "dry", "Q1"
    year = Column(Integer, index=True, nullable=False)

    total_area = Column(Float)     # hectares
    total_yield = Column(Float)    # tonnes
    average_yield = Column(Float)  # tonnes / hectare

    farms_count = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    region = relationship("Region")


# ============================================================
# REGIONAL LIVESTOCK PRODUCTION STATISTICS
# ============================================================

class RegionalLivestockStat(Base):
    __tablename__ = "regional_livestock_stats"

    id = Column(Integer, primary_key=True)

    region_id = Column(Integer, ForeignKey("regions.id"), index=True, nullable=False)

    livestock_type = Column(String, index=True, nullable=False)  # cattle, goats, poultry
    season = Column(String, nullable=False)
    year = Column(Integer, index=True, nullable=False)

    total_animals = Column(Integer)
    mortality_rate = Column(Float)   # %
    production_output = Column(Float)  # milk (litres), meat (kg), eggs (units)

    created_at = Column(DateTime, default=datetime.utcnow)

    region = relationship("Region")


# ============================================================
# REGIONAL DISEASE & PEST PREVALENCE
# ============================================================

class RegionalDiseaseStat(Base):
    __tablename__ = "regional_disease_stats"

    id = Column(Integer, primary_key=True)

    region_id = Column(Integer, ForeignKey("regions.id"), index=True, nullable=False)

    disease_or_pest = Column(String, index=True, nullable=False)
    category = Column(String)  # crop_disease, livestock_disease, pest

    season = Column(String, nullable=False)
    year = Column(Integer, index=True, nullable=False)

    affected_farms = Column(Integer)
    severity_index = Column(Float)  # normalized 0–1 or 0–10 scale

    created_at = Column(DateTime, default=datetime.utcnow)

    region = relationship("Region")


# ============================================================
# REGIONAL INPUT CONSUMPTION (FERTILIZER, FEED, VACCINE, ETC.)
# ============================================================

class RegionalInputUsageStat(Base):
    __tablename__ = "regional_input_usage"

    id = Column(Integer, primary_key=True)

    region_id = Column(Integer, ForeignKey("regions.id"), index=True, nullable=False)

    input_type = Column(String, index=True, nullable=False)  # fertilizer, feed, vaccine
    input_name = Column(String, nullable=True)  # optional: brand or formulation

    season = Column(String, nullable=False)
    year = Column(Integer, index=True, nullable=False)

    total_quantity = Column(Float)
    unit = Column(String)  # kg, litres, doses

    farms_count = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    region = relationship("Region")
