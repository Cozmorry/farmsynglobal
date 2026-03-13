from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from backend.core.database import get_db
from . import services
from .schemas import WeatherSnapshotRead

router = APIRouter(tags=["Weather"])

# ------------------------------------------------
# CURRENT WEATHER (FETCH + STORE)
# ------------------------------------------------
@router.get("/farm/{farm_id}/current", response_model=WeatherSnapshotRead)
def get_current_weather(farm_id: int, db: Session = Depends(get_db)):
    weather = services.fetch_current_weather(db, farm_id)
    if not weather:
        raise HTTPException(status_code=404, detail="Farm not found or weather unavailable")

    snapshot = services.save_weather_snapshot(db, farm_id, weather)
    return snapshot

# ------------------------------------------------
# WEATHER HISTORY
# ------------------------------------------------
@router.get("/farm/{farm_id}/history", response_model=list[WeatherSnapshotRead])
def weather_history(
    farm_id: int,
    period: str = "7d",  # 7d, 14d, 1m, 3m, 6m, 1y
    db: Session = Depends(get_db)
):
    mapping = {
        "7d": 7,
        "14d": 14,
        "1m": 30,
        "3m": 90,
        "6m": 180,
        "1y": 365,
    }

    days = mapping.get(period)
    if not days:
        raise HTTPException(status_code=400, detail="Invalid period")

    return services.get_weather_history(db, farm_id, days)

