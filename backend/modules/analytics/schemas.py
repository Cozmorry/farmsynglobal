# backend/modules/analytics/schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


# ============================================================
# BASE ANALYTICS SCHEMA
# ============================================================

class AnalyticsBase(BaseModel):
    region_id: int = Field(..., description="Region ID")
    season: Optional[str] = Field(None, description="Season or period")
    year: int = Field(..., description="Year of the statistics")
    farm_count: int = Field(..., description="Number of farms used in calculation")
    generated_on: date = Field(..., description="Date the analytics was generated")


# ============================================================
# CROP PRODUCTION
# ============================================================

class RegionalCropStatBase(AnalyticsBase):
    crop_type: str = Field(..., description="Crop type")
    total_area: float = Field(..., description="Total area planted (hectares)")
    total_yield: float = Field(..., description="Total yield (tonnes)")
    average_yield: float = Field(..., description="Average yield (tonnes/hectare)")


class RegionalCropStatRead(RegionalCropStatBase):
    id: int

    class Config:
        from_attributes = True



# ============================================================
# LIVESTOCK PRODUCTION
# ============================================================

class RegionalLivestockStatBase(AnalyticsBase):
    livestock_type: str = Field(..., description="Type of livestock (cattle, poultry, etc.)")
    total_animals: Optional[int] = Field(None, description="Total number of animals")
    mortality_rate: Optional[float] = Field(None, description="Mortality rate (%)")


class RegionalLivestockStatRead(RegionalLivestockStatBase):
    id: int

    class Config:
        from_attributes = True



# ============================================================
# INPUT USAGE
# ============================================================

class RegionalInputUsageStatBase(AnalyticsBase):
    input_type: str = Field(..., description="Type of input (fertilizer, feed, vaccine, etc.)")
    total_quantity: Optional[float] = Field(None, description="Total quantity used")
    unit: Optional[str] = Field(None, description="Unit of measurement (kg, litres, doses)")


class RegionalInputUsageStatRead(RegionalInputUsageStatBase):
    id: int

    class Config:
        from_attributes = True



# ============================================================
# DISEASE & PESTS
# ============================================================

class RegionalDiseaseStatBase(AnalyticsBase):
    disease_name: str = Field(..., description="Name of disease or pest")
    reported_cases: Optional[int] = Field(None, description="Number of affected farms")
    severity_index: Optional[float] = Field(None, description="Normalized severity (0–1 or 0–10)")


class RegionalDiseaseStatRead(RegionalDiseaseStatBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# COST OF PRODUCTION
# ============================================================

class RegionalCostStatBase(AnalyticsBase):
    commodity: str = Field(..., description="Commodity name")
    avg_cost_per_unit: float = Field(..., description="Average cost per unit")
    unit: Optional[str] = Field(None, description="Unit of measurement (kg, litre, etc.)")


class RegionalCostStatRead(RegionalCostStatBase):
    id: int

    class Config:
        from_attributes = True
