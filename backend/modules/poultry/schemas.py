#backend/modules/poultry/schemas.py
from datetime import date
from typing import Optional
from pydantic import BaseModel

# ============================================================
# 🐔 Poultry Batch Schemas
# ============================================================

class PoultryBatchBase(BaseModel):
    batch_name: str
    breed: Optional[str] = None
    batch_size: Optional[int] = None
    farm_id: Optional[int] = None
    start_date: Optional[date] = None
    housing_type: Optional[str] = None
    purpose: Optional[str] = None
    source: Optional[str] = None
    expected_cycle_days: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[str] = "Active"


class PoultryBatchCreate(PoultryBatchBase):
    pass


class PoultryBatchUpdate(BaseModel):
    batch_name: Optional[str] = None
    breed: Optional[str] = None
    batch_size: Optional[int] = None
    farm_id: Optional[int] = None
    start_date: Optional[date] = None
    housing_type: Optional[str] = None
    purpose: Optional[str] = None
    source: Optional[str] = None
    expected_cycle_days: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class PoultryBatchRead(PoultryBatchBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# 🧾 Poultry Activity Schemas
# ============================================================

class PoultryActivityBase(BaseModel):
    poultry_batch_id: int
    date: Optional[date] = None
    activity_type: str
    description: Optional[str] = None
    performed_by: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    feed_used_kg: Optional[float] = None
    water_used_l: Optional[float] = None
    mortality: Optional[int] = 0


class PoultryActivityCreate(PoultryActivityBase):
    pass


class PoultryActivityUpdate(BaseModel):
    date: Optional[date] = None
    activity_type: Optional[str] = None
    description: Optional[str] = None
    performed_by: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    feed_used_kg: Optional[float] = None
    water_used_l: Optional[float] = None
    mortality: Optional[int] = None


class PoultryActivityRead(PoultryActivityBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# 🥚 Poultry Production Schemas
# ============================================================

class PoultryProductionBase(BaseModel):
    poultry_batch_id: int
    production_type: str
    date: Optional[date] = None
    quantity: float
    unit_price: Optional[float] = 0.0
    quality_grade: Optional[str] = None
    remarks: Optional[str] = None


class PoultryProductionCreate(PoultryProductionBase):
    pass


class PoultryProductionUpdate(BaseModel):
    production_type: Optional[str] = None
    date: Optional[date] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    quality_grade: Optional[str] = None
    remarks: Optional[str] = None


class PoultryProductionRead(PoultryProductionBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# 💵 Poultry Sales Schemas
# ============================================================

class PoultrySaleBase(BaseModel):
    poultry_batch_id: int
    sale_type: str
    quantity: float
    unit_price: float
    sale_date: Optional[date] = None
    buyer_name: Optional[str] = None
    payment_status: Optional[str] = "Pending"


class PoultrySaleCreate(PoultrySaleBase):
    pass


class PoultrySaleUpdate(BaseModel):
    sale_type: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    sale_date: Optional[date] = None
    buyer_name: Optional[str] = None
    payment_status: Optional[str] = None


class PoultrySaleRead(PoultrySaleBase):
    id: int
    total_amount: float

    class Config:
        from_attributes = True

