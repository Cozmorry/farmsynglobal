#backend/modules/finance/schemas.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from enum import Enum
from backend.modules.finance.models import ModuleType


# ============================================================
# BASE FINANCE ENTRY (UNIFIED)
# ============================================================
class BaseFinanceEntryCreate(BaseModel):
    description: str
    amount: float
    category: str                  # income | expense
    farm_id: int
    module_type: ModuleType

    source: Optional[str] = "Manual Entry"
    date: Optional[date] = None
    receipt_file: Optional[str] = None
    uploaded_by: Optional[str] = None
    linked_entity_id: Optional[int] = None

    # Optional module-specific linking
    crop_id: Optional[int] = None
    block_id: Optional[int] = None
    livestock_id: Optional[int] = None
    poultry_id: Optional[int] = None
    aquaculture_id: Optional[int] = None


class BaseFinanceEntrySchema(BaseFinanceEntryCreate):
    id: int
    upload_date: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================
# FINANCIAL SUMMARY (ADDED MISSING SCHEMA)
# ============================================================
class FinancialSummary(BaseModel):
    farm_id: int

    block_id: Optional[int] = None
    crop_id: Optional[int] = None
    livestock_id: Optional[int] = None
    poultry_id: Optional[int] = None
    aquaculture_id: Optional[int] = None

    total_income: float
    total_expense: float
    profit: float


# ============================================================
# CROP FINANCE SCHEMAS
# ============================================================
class FinanceCropCreate(BaseModel):
    base_id: int
    crop_id: int
    block_id: int


class FinanceCropSchema(FinanceCropCreate):
    id: int
    base: BaseFinanceEntrySchema
    class Config:
        from_attributes = True


# ============================================================
# LIVESTOCK FINANCE SCHEMAS
# ============================================================
class FinanceLivestockCreate(BaseModel):
    base_id: int
    livestock_id: int
    reference_id: Optional[int] = None


class FinanceLivestockSchema(FinanceLivestockCreate):
    id: int
    base: BaseFinanceEntrySchema
    class Config:
        from_attributes = True


# ============================================================
# POULTRY FINANCE SCHEMAS
# ============================================================
class FinancePoultryCreate(BaseModel):
    base_id: int
    poultry_id: int
    reference_id: Optional[int] = None


class FinancePoultrySchema(FinancePoultryCreate):
    id: int
    base: BaseFinanceEntrySchema
    class Config:
        from_attributes = True


# ============================================================
# AQUACULTURE FINANCE SCHEMAS
# ============================================================
class FinanceAquacultureCreate(BaseModel):
    base_id: int
    aquaculture_id: int
    reference_id: Optional[int] = None


class FinanceAquacultureSchema(FinanceAquacultureCreate):
    id: int
    base: BaseFinanceEntrySchema
    class Config:
        from_attributes = True

# ============================================================
# HR FINANCE
# ============================================================
class FinanceHRCreate(BaseModel):
    base_id: int
    staff_id: int
    reference_id: Optional[int] = None


class FinanceHRSchema(FinanceHRCreate):
    id: int
    base: BaseFinanceEntrySchema
    class Config:
        from_attributes = True


# ============================================================
# STORE FINANCE
# ============================================================
class FinanceInventoryCreate(BaseModel):
    base_id: int
    transaction_id: int


class FinanceInventorySchema(FinanceInventoryCreate):
    id: int
    base: BaseFinanceEntrySchema
    class Config:
        from_attributes = True


# ============================================================
# PROFIT & LOSS
# ============================================================
class ProfitLossSchema(BaseModel):
    id: int
    farm_id: int
    total_income: float
    total_expense: float
    net_profit: float
    class Config:
        from_attributes = True


# ============================================================
# INVOICE
# ============================================================
class InvoiceCreate(BaseModel):
    invoice_number: str
    description: Optional[str] = None
    amount: float
    date_issued: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = "unpaid"
    farm_id: Optional[int] = None


class InvoiceSchema(InvoiceCreate):
    id: int
    class Config:
        from_attributes = True


# ============================================================
# PAYMENT
# ============================================================
class PaymentCreate(BaseModel):
    payment_reference: str
    amount: float
    date_paid: Optional[date] = None
    method: Optional[str] = "cash"
    invoice_id: Optional[int] = None
    farm_id: Optional[int] = None


class PaymentSchema(PaymentCreate):
    id: int
    class Config:
        from_attributes = True
