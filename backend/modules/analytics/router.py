# backend/modules/analytics/router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from backend.core.database import get_db
from . import services, models

router = APIRouter(tags=["Analytics"])

# ============================================================
# CROP PRODUCTION
# ============================================================

@router.post("/crops/aggregate")
def aggregate_crops(
    region_id: int = Query(..., description="Region ID to aggregate"),
    crop_type: str = Query(..., description="Crop type"),
    season: str = Query(..., description="Season or period"),
    year: int = Query(..., description="Year of aggregation"),
    db: Session = Depends(get_db),
):
    stat = services.aggregate_crop_production(db, region_id, crop_type, season, year)
    if not stat:
        raise HTTPException(status_code=404, detail="Not enough data to aggregate")
    return stat


@router.get("/crops")
def get_crop_stats(
    region_id: int,
    crop_type: str,
    season: str,
    year: int,
    db: Session = Depends(get_db),
):
    stat = db.query(models.RegionalCropStat).filter_by(
        region_id=region_id, crop_type=crop_type, season=season, year=year
    ).first()
    if not stat:
        raise HTTPException(status_code=404, detail="No statistics found")
    return stat


# ============================================================
# LIVESTOCK PRODUCTION
# ============================================================

@router.post("/livestock/aggregate")
def aggregate_livestock(
    region_id: int,
    livestock_type: str,
    season: str,
    year: int,
    db: Session = Depends(get_db),
):
    stat = services.aggregate_livestock_production(db, region_id, livestock_type, season, year)
    if not stat:
        raise HTTPException(status_code=404, detail="Not enough data to aggregate")
    return stat


@router.get("/livestock")
def get_livestock_stats(
    region_id: int,
    livestock_type: str,
    season: str,
    year: int,
    db: Session = Depends(get_db),
):
    stat = db.query(models.RegionalLivestockStat).filter_by(
        region_id=region_id, livestock_type=livestock_type, season=season, year=year
    ).first()
    if not stat:
        raise HTTPException(status_code=404, detail="No statistics found")
    return stat


# ============================================================
# INPUT USAGE
# ============================================================

@router.post("/inputs/aggregate")
def aggregate_inputs(
    region_id: int,
    input_type: str,
    season: str,
    year: int,
    db: Session = Depends(get_db),
):
    stat = services.aggregate_input_usage(db, region_id, input_type, season, year)
    if not stat:
        raise HTTPException(status_code=404, detail="Not enough data to aggregate")
    return stat


@router.get("/inputs")
def get_input_stats(
    region_id: int,
    input_type: str,
    season: str,
    year: int,
    db: Session = Depends(get_db),
):
    stat = db.query(models.RegionalInputUsageStat).filter_by(
        region_id=region_id, input_type=input_type, season=season, year=year
    ).first()
    if not stat:
        raise HTTPException(status_code=404, detail="No statistics found")
    return stat


# ============================================================
# DISEASES & PESTS
# ============================================================

@router.post("/diseases/aggregate")
def aggregate_diseases(
    region_id: int,
    disease_name: str,
    season: str,
    year: int,
    db: Session = Depends(get_db),
):
    stat = services.aggregate_disease_stats(db, region_id, disease_name, season, year)
    if not stat:
        raise HTTPException(status_code=404, detail="Not enough data to aggregate")
    return stat


@router.get("/diseases")
def get_disease_stats(
    region_id: int,
    disease_name: str,
    season: str,
    year: int,
    db: Session = Depends(get_db),
):
    stat = db.query(models.RegionalDiseaseStat).filter_by(
        region_id=region_id, disease_name=disease_name, season=season, year=year
    ).first()
    if not stat:
        raise HTTPException(status_code=404, detail="No statistics found")
    return stat


# ============================================================
# COST OF PRODUCTION
# ============================================================

@router.post("/costs/aggregate")
def aggregate_costs(
    region_id: int,
    commodity: str,
    season: str,
    year: int,
    avg_cost_per_unit: float,
    farm_count: int,
    db: Session = Depends(get_db),
):
    stat = services.aggregate_cost_stats(db, region_id, commodity, season, year, avg_cost_per_unit, farm_count)
    if not stat:
        raise HTTPException(status_code=404, detail="Not enough data to aggregate")
    return stat


@router.get("/costs")
def get_cost_stats(
    region_id: int,
    commodity: str,
    season: str,
    year: int,
    db: Session = Depends(get_db),
):
    stat = db.query(models.RegionalCostStat).filter_by(
        region_id=region_id, commodity=commodity, season=season, year=year
    ).first()
    if not stat:
        raise HTTPException(status_code=404, detail="No statistics found")
    return stat
