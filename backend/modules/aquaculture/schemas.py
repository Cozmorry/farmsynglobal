from typing import Optional, List
from datetime import date
from pydantic import BaseModel

# ============================
# 🌊 AQUACULTURE POND SCHEMAS
# ============================
class AquacultureBase(BaseModel):
    pond_name: str
    species: str
    pond_size: Optional[float] = None
    stock_quantity: Optional[int] = None
    average_weight: Optional[float] = 0.0
    date_stocked: Optional[date] = None
    farm_id: Optional[int] = None
    feed_type: Optional[str] = None
    feed_cost: Optional[float] = None
    water_quality_status: Optional[str] = None

class AquacultureCreate(AquacultureBase):
    pass

class AquacultureUpdate(BaseModel):
    pond_name: Optional[str] = None
    species: Optional[str] = None
    pond_size: Optional[float] = None
    stock_quantity: Optional[int] = None
    average_weight: Optional[float] = None
    date_stocked: Optional[date] = None
    farm_id: Optional[int] = None
    feed_type: Optional[str] = None
    feed_cost: Optional[float] = None
    water_quality_status: Optional[str] = None

class AquacultureRead(AquacultureBase):
    id: int
    class Config:
        from_attributes = True

# ============================
# 🍽 FEEDING SCHEMAS
# ============================
class AquacultureFeedingBase(BaseModel):
    pond_id: int
    date: Optional[date] = None
    feed_quantity: float
    feed_type: Optional[str] = None
    remarks: Optional[str] = None

class AquacultureFeedingCreate(AquacultureFeedingBase):
    pass

class AquacultureFeedingUpdate(BaseModel):
    date: Optional[date] = None
    feed_quantity: Optional[float] = None
    feed_type: Optional[str] = None
    remarks: Optional[str] = None

class AquacultureFeedingRead(AquacultureFeedingBase):
    id: int
    class Config:
        from_attributes = True

# ============================
# 💧 WATER QUALITY SCHEMAS
# ============================
class AquacultureWaterQualityBase(BaseModel):
    pond_id: int
    date: Optional[date] = None
    temperature: Optional[float] = None
    ph_level: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    ammonia: Optional[float] = None
    turbidity: Optional[float] = None
    notes: Optional[str] = None

class AquacultureWaterQualityCreate(AquacultureWaterQualityBase):
    pass

class AquacultureWaterQualityUpdate(BaseModel):
    date: Optional[date] = None
    temperature: Optional[float] = None
    ph_level: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    ammonia: Optional[float] = None
    turbidity: Optional[float] = None
    notes: Optional[str] = None

class AquacultureWaterQualityRead(AquacultureWaterQualityBase):
    id: int
    class Config:
        from_attributes = True

# ============================
# 🐟 HARVEST SCHEMAS
# ============================
class AquacultureHarvestBase(BaseModel):
    pond_id: int
    date: Optional[date] = None
    total_weight: float
    average_weight: Optional[float] = None
    mortality: Optional[int] = None
    remarks: Optional[str] = None

class AquacultureHarvestCreate(AquacultureHarvestBase):
    pass

class AquacultureHarvestUpdate(BaseModel):
    date: Optional[date] = None
    total_weight: Optional[float] = None
    average_weight: Optional[float] = None
    mortality: Optional[int] = None
    remarks: Optional[str] = None

class AquacultureHarvestRead(AquacultureHarvestBase):
    id: int
    class Config:
        from_attributes = True

# ============================
# ⚡ ACTIVITY SCHEMAS
# ============================
class AquacultureActivityBase(BaseModel):
    aquaculture_id: int
    activity_type: str
    date: Optional[date] = None
    description: Optional[str] = None
    performed_by: Optional[str] = None
    cost: Optional[float] = 0.0

class AquacultureActivityCreate(AquacultureActivityBase):
    pass

class AquacultureActivityUpdate(BaseModel):
    activity_type: Optional[str] = None
    date: Optional[date] = None
    description: Optional[str] = None
    performed_by: Optional[str] = None
    cost: Optional[float] = None

class AquacultureActivityRead(AquacultureActivityBase):
    id: int
    class Config:
        from_attributes = True

# ============================
# 🎯 PRODUCTION SCHEMAS
# ============================
class AquacultureProductionBase(BaseModel):
    aquaculture_id: int
    production_type: str
    quantity: float
    unit_price: Optional[float] = 0.0
    total_value: Optional[float] = 0.0
    date: Optional[date] = None

class AquacultureProductionCreate(AquacultureProductionBase):
    pass

class AquacultureProductionUpdate(BaseModel):
    production_type: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_value: Optional[float] = None
    date: Optional[date] = None

class AquacultureProductionRead(AquacultureProductionBase):
    id: int
    class Config:
        from_attributes = True

# ============================
# 📊 SUMMARY SCHEMAS
# ============================
class AquacultureSummaryBase(BaseModel):
    pond_id: int
    date: Optional[date] = None
    total_feed: Optional[float] = 0.0
    average_temp: Optional[float] = 0.0
    average_ph: Optional[float] = 0.0
    average_oxygen: Optional[float] = 0.0
    mortality_rate: Optional[float] = 0.0
    growth_rate: Optional[float] = 0.0
    fcr: Optional[float] = 0.0
    notes: Optional[str] = None

class AquacultureSummaryCreate(AquacultureSummaryBase):
    pass

class AquacultureSummaryUpdate(BaseModel):
    date: Optional[date] = None
    total_feed: Optional[float] = None
    average_temp: Optional[float] = None
    average_ph: Optional[float] = None
    average_oxygen: Optional[float] = None
    mortality_rate: Optional[float] = None
    growth_rate: Optional[float] = None
    fcr: Optional[float] = None
    notes: Optional[str] = None

class AquacultureSummaryRead(AquacultureSummaryBase):
    id: int
    class Config:
        from_attributes = True




