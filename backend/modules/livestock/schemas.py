# backend/modules/livestock/schemas.py

from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from enum import Enum

# =====================================================
# ENUMS
# =====================================================
class LivestockTypeEnum(str, Enum):
    CATTLE = "Cattle"
    SHEEP = "Sheep"
    GOAT = "Goat"
    PIG = "Pig"
    OTHER = "Other"


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class LivestockStatusEnum(str, Enum):
    ACTIVE = "active"
    SOLD = "sold"
    SLAUGHTERED = "slaughtered"
    DECEASED = "deceased"


class FeedingMethodEnum(str, Enum):
    PASTURE = "pasture"
    STALL = "stall"
    MIXED = "mixed"


class ActivityTypeEnum(str, Enum):
    SERVICE = "service"
    CONSUMABLE = "consumable"


class ActivityCategoryEnum(str, Enum):
    HEALTH = "health"
    BREEDING = "breeding"
    MANAGEMENT = "management"


class ProductionTypeEnum(str, Enum):
    MILK = "Milk"
    MEAT = "Meat"
    MANURE = "Manure"
    GENERIC = "Generic"


# =====================================================
# LIVESTOCK
# =====================================================
class LivestockBase(BaseModel):
    name: str
    tag_number: Optional[str] = None
    type: LivestockTypeEnum
    breed: Optional[str] = None
    gender: GenderEnum
    date_of_birth: Optional[date] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = 0.0
    farm_id: int
    barn_id: Optional[int] = None
    group_id: Optional[int] = None
    status: LivestockStatusEnum = LivestockStatusEnum.ACTIVE
    remarks: Optional[str] = None


class LivestockCreate(LivestockBase):
    pass


class LivestockUpdate(BaseModel):
    name: Optional[str] = None
    tag_number: Optional[str] = None
    type: Optional[LivestockTypeEnum] = None
    breed: Optional[str] = None
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = None
    barn_id: Optional[int] = None
    group_id: Optional[int] = None
    status: Optional[LivestockStatusEnum] = None
    remarks: Optional[str] = None


class LivestockRead(LivestockBase):
    id: int

    class Config:
        from_attributes = True


# =====================================================
# LIVESTOCK GROUP / HERD
# =====================================================
class LivestockGroupBase(BaseModel):
    name: str
    farm_id: int
    description: Optional[str] = None


class LivestockGroupCreate(LivestockGroupBase):
    pass


class LivestockGroupRead(LivestockGroupBase):
    id: int

    class Config:
        from_attributes = True


# =====================================================
# WEIGHT RECORDS
# =====================================================
class LivestockWeightRecordBase(BaseModel):
    livestock_id: int
    weight: float
    date_recorded: Optional[date] = None


class LivestockWeightRecordCreate(LivestockWeightRecordBase):
    pass


class LivestockWeightRecordRead(LivestockWeightRecordBase):
    id: int

    class Config:
        from_attributes = True


# =====================================================
# FEEDING
# =====================================================
class LivestockFeedingBase(BaseModel):
    livestock_id: Optional[int] = None
    group_id: Optional[int] = None
    feed_item_id: int
    feeding_method: FeedingMethodEnum
    quantity: float
    feeding_date: Optional[date] = None
    remarks: Optional[str] = None

    inventory_transaction_id: int
    hr_work_session_id: Optional[int] = None

    feeding_date: Optional[date] = None
    remarks: Optional[str] = None

class LivestockFeedingCreate(LivestockFeedingBase):
    pass


class LivestockFeedingRead(LivestockFeedingBase):
    id: int
   
    class Config:
        from_attributes = True


# =====================================================
# ACTIVITIES
# =====================================================
class LivestockActivityBase(BaseModel):
    livestock_id: int
    name: str
    description: Optional[str] = None
    activity_type: ActivityTypeEnum
    activity_category: ActivityCategoryEnum
    performed_by: Optional[str] = None
    store_item_id: Optional[int] = None
    quantity_used: Optional[float] = None
    date_performed: Optional[date] = None
    remarks: Optional[str] = None

    inventory_transaction_id: int
    hr_work_session_id: Optional[int] = None



class LivestockActivityCreate(LivestockActivityBase):
    pass


class LivestockActivityRead(LivestockActivityBase):
    id: int
    total_cost: Optional[float] = None

    class Config:
        from_attributes = True


# =====================================================
# PRODUCTION
# =====================================================
class LivestockProductionBase(BaseModel):
    livestock_id: int
    production_type: ProductionTypeEnum
    quantity: float
    fat_content: Optional[float] = None
    carcass_weight: Optional[float] = None
    date_recorded: Optional[date] = None
    remarks: Optional[str] = None


class LivestockProductionCreate(LivestockProductionBase):
    pass


class LivestockProductionRead(LivestockProductionBase):
    id: int

    class Config:
        from_attributes = True

# =====================================================
# SALES
# =====================================================
class LivestockSaleBase(BaseModel):
    livestock_id: int
    production_id: Optional[int] = None
    quantity: float
    unit_price: float
    buyer_name: Optional[str] = None
    payment_status: Optional[str] = "paid"
    date: Optional[date] = None


class LivestockSaleCreate(LivestockSaleBase):
    pass


class LivestockSaleRead(LivestockSaleBase):
    id: int
    total_sale: float

    class Config:
        from_attributes = True


# =====================================================
# BREEDING
# =====================================================
class LivestockBreedingBase(BaseModel):
    dam_id: int
    sire_id: Optional[int] = None
    service_date: date
    method: Optional[str] = None
    expected_birth_date: Optional[date] = None
    actual_birth_date: Optional[date] = None
    offspring_count: Optional[int] = None
    remarks: Optional[str] = None


class LivestockBreedingCreate(LivestockBreedingBase):
    pass


class LivestockBreedingRead(LivestockBreedingBase):
    id: int

    class Config:
        from_attributes = True


# =====================================================
# EXPENSES
# =====================================================
class LivestockExpenseBase(BaseModel):
    livestock_id: int
    category: Optional[str] = "Livestock"
    sub_category: Optional[str] = None
    amount: float
    date: Optional[date] = None


class LivestockExpenseCreate(LivestockExpenseBase):
    pass


class LivestockExpenseRead(LivestockExpenseBase):
    id: int

    class Config:
        from_attributes = True


# =====================================================
# EXTENDED LIVESTOCK VIEW
# =====================================================
class LivestockDetailRead(LivestockRead):
    feedings: List[LivestockFeedingRead] = []
    activities: List[LivestockActivityRead] = []
    productions: List[LivestockProductionRead] = []
    sales: List[LivestockSaleRead] = []
    weight_records: List[LivestockWeightRecordRead] = []

    breedings_as_dam: List[LivestockBreedingRead] = []
    breedings_as_sire: List[LivestockBreedingRead] = []

    class Config:
        from_attributes = True

