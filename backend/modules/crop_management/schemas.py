# backend/modules/crop_management/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum


# ============================================================
# ENUMS (MATCH FRONTEND ROUTES)
# ============================================================

class ActivityType(str, Enum):
    scouting = "scouting-activities"
    weeding = "weeding-activities"
    fertilizer = "fertilizer-applications"
    chemical = "chemical-applications"
    irrigation = "irrigation"
    nursery = "nursery-activities"
    land_preparation = "land-preparation"
    crop_rotation = "crop-rotations"
    harvest = "harvests"
    sale = "sales"


# ============================================================
# FARM
# ============================================================

class FarmRead(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        from_attributes = True


# ============================================================
# BLOCK
# ============================================================

class BlockRead(BaseModel):
    id: int
    name: str
    area: float
    farm_id: int

    class Config:
        from_attributes = True


# ============================================================
# CROP
# ============================================================

class CropBase(BaseModel):
    name: str
    variety: Optional[str]
    farm_id: int
    block_id: int
    planting_date: Optional[date]
    season_start: Optional[date]
    season_end: Optional[date]
    status: Optional[str]


class CropCreate(CropBase):
    pass


class CropRead(CropBase):
    id: int
    farm: FarmRead
    block: BlockRead

    class Config:
        from_attributes = True

# ============================================================
# HR-LINKED ACTIVITY BASE
# ============================================================

class HRLinkedActivityBase(BaseModel):
    """
    Labour is always recorded in HR.
    Crop activities only reference HR work sessions.
    """
    hr_work_session_id: Optional[int] = None
    

# ============================================================



# ============================================================
# NURSERY ACTIVITIES
# ============================================================

class NurseryActivityBase(BaseModel):
    planted_date: date
    germination_rate: Optional[float]
    materials_used: Optional[str]
    tentative_transplant_date: Optional[date]
   

class NurseryActivityCreate(NurseryActivityBase):
    crop_id: int


class NurseryActivityRead(NurseryActivityBase):
    id: int
    crop_id: int
    crop: CropRead

    class Config:
        from_attributes = True


# ============================================================
# GENERAL CROP ACTIVITIES
# ============================================================

class CropActivityBase(BaseModel):
    activity_type: str
    description: Optional[str]
    date: Optional[date]
   
class CropActivityCreate(CropActivityBase):
    crop_id: int
    block_id: int


class CropActivityRead(CropActivityBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# LAND PREPARATION
# ============================================================

class LandPreparationActivityBase(BaseModel):
    date: Optional[date]
    method: Optional[str]
   

class LandPreparationActivityCreate(LandPreparationActivityBase):
    crop_id: int
    block_id: int


class LandPreparationActivityRead(LandPreparationActivityBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# IRRIGATION
# ============================================================

class IrrigationBase(BaseModel):
    date: Optional[date]
    method: Optional[str]
    duration_hours: Optional[float]
    

class IrrigationCreate(IrrigationBase):
    crop_id: int
    block_id: int


class IrrigationRead(IrrigationBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True

# ============================================================
# FERTILIZER APPLICATIONS
# ============================================================

class FertilizerApplicationBase(BaseModel):
    fertilizer_name: Optional[str]
    quantity_kg: Optional[float]
    date: Optional[date]


class FertilizerApplicationCreate(FertilizerApplicationBase):
    crop_id: int
    block_id: int


class FertilizerApplicationRead(FertilizerApplicationBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# CHEMICAL APPLICATIONS
# ============================================================

class ChemicalApplicationBase(BaseModel):
    chemical_name: Optional[str]
    quantity_ltr: Optional[float]
    date: Optional[date]


class ChemicalApplicationCreate(ChemicalApplicationBase):
    crop_id: int
    block_id: int


class ChemicalApplicationRead(ChemicalApplicationBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# WEEDING ACTIVITIES
# ============================================================

class WeedingActivityBase(BaseModel):
    date: Optional[date]
    method: Optional[str]
    

class WeedingActivityCreate(WeedingActivityBase):
    crop_id: int
    block_id: int


class WeedingActivityRead(WeedingActivityBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# SCOUTING ACTIVITIES
# ============================================================

class ScoutingActivityBase(BaseModel):
    date: Optional[date]
    pests: Optional[str]
    diseases: Optional[str]
    nutrient_deficiency: Optional[str]
    notes: Optional[str]



class ScoutingActivityCreate(ScoutingActivityBase):
    crop_id: int
    block_id: int


class ScoutingActivityRead(ScoutingActivityBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# SOIL TESTS
# ============================================================

class SoilTestBase(BaseModel):
    date: Optional[date]
    ph: Optional[float]
    ec: Optional[float]
    n: Optional[float]
    p: Optional[float]
    k: Optional[float]
    micronutrients: Optional[str]
    lab_report: Optional[str]


class SoilTestCreate(SoilTestBase):
    crop_id: int
    block_id: int


class SoilTestRead(SoilTestBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# SOIL AMENDMENTS
# ============================================================

class SoilAmendmentBase(BaseModel):
    amendment_type: Optional[str]
    quantity: Optional[float]
    date: Optional[date]


class SoilAmendmentCreate(SoilAmendmentBase):
    crop_id: int
    block_id: int


class SoilAmendmentRead(SoilAmendmentBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# CROP ROTATIONS
# ============================================================

class CropRotationBase(BaseModel):
    previous_crop: Optional[str]
    next_crop: Optional[str]
    rotation_start: Optional[date]
    rotation_end: Optional[date]
    notes: Optional[str]


class CropRotationCreate(CropRotationBase):
    farm_id: int
    block_id: int
    crop_id: int


class CropRotationRead(CropRotationBase):
    id: int
    farm_id: int
    block_id: int
    crop_id: int
    farm: FarmRead
    block: BlockRead
    crop: CropRead

    class Config:
        from_attributes = True

# ============================================================
# HARVESTS
# ============================================================

class CropHarvestBase(BaseModel):
    harvest_date: Optional[date]
    field_weight: Optional[float]
    final_weight: Optional[float]
    moisture_content: Optional[float]
    grade_a: Optional[float]
    grade_b: Optional[float]
    grade_c: Optional[float]
    rejects: Optional[float]
    

class CropHarvestCreate(CropHarvestBase):
    crop_id: int
    block_id: int


class CropHarvestRead(CropHarvestBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# SALES
# ============================================================

class CropSaleBase(BaseModel):
    sale_date: Optional[date]
    quantity_sold: Optional[float]
    grade_a: Optional[float]
    grade_b: Optional[float]
    grade_c: Optional[float]
    rejects_returned: Optional[float]
    price_per_unit: Optional[float]
    buyer: Optional[str]
    income: Optional[float] = None


class CropSaleCreate(CropSaleBase):
    crop_id: int
    block_id: int


class CropSaleRead(CropSaleBase):
    id: int
    crop_id: int
    block_id: int
    crop: CropRead
    block: BlockRead

    class Config:
        from_attributes = True


# ============================================================
# ACTIVITY UPLOADS
# ============================================================

class CropActivityUploadBase(BaseModel):
    activity_type: ActivityType
    activity_id: int
    file_type: Optional[str]
    description: Optional[str]


class CropActivityUploadCreate(CropActivityUploadBase):
    crop_id: int


class CropActivityUploadRead(CropActivityUploadBase):
    id: int
    crop_id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# FINAL CROP SUMMARY
# ============================================================
class FinalCropSummaryRead(BaseModel):
    final_yield: float
    final_weight: float
    total_cost: float
    total_sale_value: float
    profit_or_loss: float

    class Config:
        from_attributes = True
