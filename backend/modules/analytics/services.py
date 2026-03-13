# backend/modules/analytics/services.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date

from backend.modules.farms.models import Farm
from backend.modules.crop_management.models import CropHarvest
from backend.modules.livestock.models import Livestock
from backend.modules.inputs.models import InputUsage
from backend.modules.diseases.models import DiseaseReport
from . import models

# ============================================================
# PRIVACY & THRESHOLDS
# ============================================================
MIN_FARMS_REQUIRED = 10


# ============================================================
# CROP PRODUCTION
# ============================================================

def aggregate_crop_production(
    db: Session,
    region_id: int,
    crop_type: str,
    season: str,
    year: int,
):
    """
    Aggregates crop production statistics for a region.
    Privacy enforced: only if >= MIN_FARMS_REQUIRED.
    """

    query = (
        db.query(
            func.count(func.distinct(Farm.id)).label("farm_count"),
            func.sum(CropHarvest.area).label("total_area"),
            func.sum(CropHarvest.yield_amount).label("total_yield"),
        )
        .join(Farm, Farm.id == CropHarvest.farm_id)
        .filter(Farm.region_id == region_id)
        .filter(CropHarvest.crop_type == crop_type)
        .filter(CropHarvest.season == season)
        .filter(CropHarvest.year == year)
    )

    result = query.one()

    if not result or result.farm_count < MIN_FARMS_REQUIRED:
        return None  # privacy enforcement

    avg_yield = (
        result.total_yield / result.total_area
        if result.total_area and result.total_area > 0
        else 0
    )

    stat = models.RegionalCropStat(
        region_id=region_id,
        crop_type=crop_type,
        season=season,
        year=year,
        farm_count=result.farm_count,
        total_area=result.total_area,
        total_yield=result.total_yield,
        average_yield=avg_yield,
        generated_on=datetime.utcnow(),
    )

    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat


# ============================================================
# LIVESTOCK PRODUCTION
# ============================================================

def aggregate_livestock_production(
    db: Session,
    region_id: int,
    livestock_type: str,
    season: str,
    year: int,
):
    """
    Aggregates livestock stats for a region.
    Privacy enforced.
    """

    query = (
        db.query(
            func.count(func.distinct(Farm.id)).label("farm_count"),
            func.sum(LivestockRecord.count).label("total_animals"),
            func.avg(LivestockRecord.mortality_rate).label("avg_mortality"),
        )
        .join(Farm, Farm.id == LivestockRecord.farm_id)
        .filter(Farm.region_id == region_id)
        .filter(LivestockRecord.livestock_type == livestock_type)
        .filter(LivestockRecord.season == season)
        .filter(LivestockRecord.year == year)
    )

    result = query.one()
    if not result or result.farm_count < MIN_FARMS_REQUIRED:
        return None

    stat = models.RegionalLivestockStat(
        region_id=region_id,
        livestock_type=livestock_type,
        season=season,
        year=year,
        farm_count=result.farm_count,
        total_animals=result.total_animals or 0,
        mortality_rate=result.avg_mortality or 0,
        generated_on=datetime.utcnow(),
    )

    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat


# ============================================================
# INPUT USAGE (FERTILIZER, FEED, VACCINE, ETC.)
# ============================================================

def aggregate_input_usage(
    db: Session,
    region_id: int,
    input_type: str,
    season: str,
    year: int,
):
    query = (
        db.query(
            func.count(func.distinct(Farm.id)).label("farm_count"),
            func.sum(InputUsage.quantity).label("total_quantity"),
        )
        .join(Farm, Farm.id == InputUsage.farm_id)
        .filter(Farm.region_id == region_id)
        .filter(InputUsage.input_type == input_type)
        .filter(InputUsage.season == season)
        .filter(InputUsage.year == year)
    )

    result = query.one()
    if not result or result.farm_count < MIN_FARMS_REQUIRED:
        return None

    stat = models.RegionalInputUsageStat(
        region_id=region_id,
        input_type=input_type,
        season=season,
        year=year,
        farm_count=result.farm_count,
        total_quantity=result.total_quantity or 0,
        generated_on=datetime.utcnow(),
    )

    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat


# ============================================================
# DISEASE & PEST REPORTING
# ============================================================

def aggregate_disease_stats(
    db: Session,
    region_id: int,
    disease_name: str,
    season: str,
    year: int,
):
    query = (
        db.query(
            func.count(func.distinct(Farm.id)).label("farm_count"),
            func.sum(DiseaseReport.reported_cases).label("reported_cases"),
        )
        .join(Farm, Farm.id == DiseaseReport.farm_id)
        .filter(Farm.region_id == region_id)
        .filter(DiseaseReport.disease_name == disease_name)
        .filter(DiseaseReport.season == season)
        .filter(DiseaseReport.year == year)
    )

    result = query.one()
    if not result or result.farm_count < MIN_FARMS_REQUIRED:
        return None

    stat = models.RegionalDiseaseStat(
        region_id=region_id,
        disease_name=disease_name,
        season=season,
        year=year,
        farm_count=result.farm_count,
        reported_cases=result.reported_cases or 0,
        generated_on=datetime.utcnow(),
    )

    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat


# ============================================================
# COST OF PRODUCTION
# ============================================================

def aggregate_cost_stats(
    db: Session,
    region_id: int,
    commodity: str,
    season: str,
    year: int,
    avg_cost_per_unit: float,
    farm_count: int,
):
    """
    Aggregate cost statistics (simplified for now).
    Can be extended to calculate from actual input costs per farm.
    """
    if farm_count < MIN_FARMS_REQUIRED:
        return None

    stat = models.RegionalCostStat(
        region_id=region_id,
        commodity=commodity,
        season=season,
        year=year,
        farm_count=farm_count,
        avg_cost_per_unit=avg_cost_per_unit,
        generated_on=datetime.utcnow(),
    )

    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat
