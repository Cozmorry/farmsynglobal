from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from backend.core.database import Base
from datetime import datetime
from sqlalchemy import JSON

class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), index=True)

    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_direction = Column(Float, nullable=True)
    description = Column(String, nullable=True)

    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)

