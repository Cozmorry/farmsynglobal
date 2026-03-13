import requests
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.modules.farms import models as farm_models
from .models import WeatherSnapshot

OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"

# ------------------------------------------------
# FETCH CURRENT WEATHER FROM API
# ------------------------------------------------
def fetch_current_weather(db: Session, farm_id: int):
    farm = db.query(farm_models.Farm).filter(farm_models.Farm.id == farm_id).first()
    if not farm:
        return None

    # NOTE: you must later add latitude & longitude to Farm
    # For now assume location is usable or mocked
    lat, lon = farm.latitude, farm.longitude

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(url)
    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "rainfall": data.get("rain", {}).get("1h", 0),
        "wind_speed": data["wind"]["speed"],
        "wind_direction": data["wind"].get("deg"),
        "description": data["weather"][0]["description"],
    }

# ------------------------------------------------
# SAVE SNAPSHOT
# ------------------------------------------------
def save_weather_snapshot(db: Session, farm_id: int, weather_data: dict):
    snapshot = WeatherSnapshot(
        farm_id=farm_id,
        **weather_data
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

# ------------------------------------------------
# GET HISTORY BY PERIOD
# ------------------------------------------------
def get_weather_history(db: Session, farm_id: int, days: int):
    since = datetime.utcnow() - timedelta(days=days)

    return (
        db.query(WeatherSnapshot)
        .filter(
            WeatherSnapshot.farm_id == farm_id,
            WeatherSnapshot.recorded_at >= since
        )
        .order_by(WeatherSnapshot.recorded_at.asc())
        .all()
    )

