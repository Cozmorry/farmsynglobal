# modules/hr/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# ============================================================
# 👷 Permanent Staff
# ============================================================
class PermanentStaffBase(BaseModel):
    name: str
    position: Optional[str] = None
    salary: Optional[float] = 0.0
    module_type: Optional[str] = "mixed"

    farm_id: Optional[int] = None
    paye_rate: Optional[float] = 0.0
    contact: Optional[str] = None
    national_id: Optional[str] = None
    bank_account: Optional[str] = None
    insurance_provider: Optional[str] = None
    benefits: Optional[float] = 0.0
    deductions: Optional[float] = 0.0
    status: Optional[str] = "active"

class PermanentStaffCreate(PermanentStaffBase):
    start_date: Optional[date] = None

class PermanentStaffResponse(PermanentStaffBase):
    id: int
    start_date: date
    is_active: bool
    deleted_at: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    # Nested HR relationships
    work_sessions: Optional[List["HRWorkSessionResponse"]] = []
    payments: Optional[List["HRPaymentResponse"]] = []
    payrolls: Optional[List["PayrollResponse"]] = []

    class Config:
        from_attributes = True

# ============================================================
# 👷 Casual Worker
# ============================================================
class CasualWorkerBase(BaseModel):
    name: str
    module_type: Optional[str] = "mixed"

    daily_rate: Optional[float] = 0.0
    farm_id: Optional[int] = None
    contact: Optional[str] = None
    block_id: Optional[int] = None
    greenhouse_id: Optional[int] = None
    skill: Optional[str] = None
    status: Optional[str] = "active"

class CasualWorkerCreate(CasualWorkerBase):
    pass

class CasualWorkerResponse(CasualWorkerBase):
    id: int
    total_days_worked: int = 0
    total_pay: float = 0.0
    is_active: bool
    deleted_at: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    # Nested HR relationships
    work_sessions: Optional[List["HRWorkSessionResponse"]] = []
    payments: Optional[List["HRPaymentResponse"]] = []

    class Config:
        from_attributes = True

# ============================================================
# 🧾 HR Work Session
# ============================================================
class HRWorkSessionBase(BaseModel):
    staff_id: Optional[int] = None
    worker_type: Optional[str] = None
    module_type: Optional[str] = "mixed"

    date: Optional[date] = None
    activity: Optional[str] = None
    task_description: Optional[str] = None
    hours_worked: Optional[float] = 0.0
    wage_rate: Optional[float] = 0.0
    total_amount: Optional[float] = 0.0
    status: Optional[str] = "pending"

    farm_id: Optional[int] = None
    block_id: Optional[int] = None
    greenhouse_id: Optional[int] = None

class HRWorkSessionCreate(HRWorkSessionBase):
    pass

class HRWorkSessionResponse(HRWorkSessionBase):
    id: int
    is_active: bool
    deleted_at: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================================
# 💵 HR Payment
# ============================================================
class HRPaymentBase(BaseModel):
    staff_id: Optional[int] = None
    worker_type: Optional[str] = None
    module_type: Optional[str] = "mixed"

    farm_id: Optional[int] = None
    amount: Optional[float] = 0.0
    description: Optional[str] = None
    payment_method: Optional[str] = None
    payment_date: Optional[date] = None
    status: Optional[str] = "completed"

class HRPaymentCreate(HRPaymentBase):
    pass

class HRPaymentResponse(HRPaymentBase):
    id: int
    is_active: bool
    deleted_at: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================================
# 📅 Payroll
# ============================================================
class PayrollBase(BaseModel):
    employee_id: int
    period_start: date
    period_end: date
    gross_pay: Optional[float] = 0.0
    deductions: Optional[float] = 0.0
    net_pay: Optional[float] = 0.0
    paid_on: Optional[date] = None
    payment_method: Optional[str] = None
    reference: Optional[str] = None
    recorded_by: Optional[str] = "system"

class PayrollCreate(PayrollBase):
    pass

class PayrollResponse(PayrollBase):
    id: int
    is_active: bool
    deleted_at: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# Resolve forward references for nested models
# ============================================================
PermanentStaffResponse.update_forward_refs()
CasualWorkerResponse.update_forward_refs()
