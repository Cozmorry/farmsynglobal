from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WeatherSnapshotBase(BaseModel):
    temperature: Optional[float]
    humidity: Optional[float]
    rainfall: Optional[float]
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    description: Optional[str]

class WeatherSnapshotCreate(WeatherSnapshotBase):
    farm_id: int

class WeatherSnapshotRead(WeatherSnapshotBase):
    id: int
    farm_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True




class WeatherRead(BaseModel):
    temperature: Optional[float]
    humidity: Optional[float]
    rainfall: Optional[float]
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    description: Optional[str]

    class Config:
        from_attributes = True



