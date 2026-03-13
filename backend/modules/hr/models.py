# backend/modules/hr/models.py

import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Date, ForeignKey, Text, Boolean
)
from sqlalchemy.orm import relationship, foreign
from backend.core.database import Base
from sqlalchemy import JSON

# ============================================================
# PERMANENT STAFF
# ============================================================
class PermanentStaff(Base):
    __tablename__ = "permanent_staff"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False, index=True)
    module_type = Column(String(50), nullable=False, default="mixed")

    name = Column(String(255), nullable=False)
    position = Column(String(100))
    salary = Column(Float, default=0.0)
    paye_rate = Column(Float, default=0.0)
    contact = Column(String(100))
    national_id = Column(String(50))
    bank_account = Column(String(100))
    insurance_provider = Column(String(100))

    start_date = Column(Date, default=datetime.date.today)
    status = Column(String(50), default="active")

    benefits = Column(Float, default=0.0)
    deductions = Column(Float, default=0.0)

    is_active = Column(Boolean, default=True)
    deleted_at = Column(Date, nullable=True)

    created_at = Column(Date, default=datetime.date.today)
    updated_at = Column(Date, default=datetime.date.today, onupdate=datetime.date.today)

    # Relationships
    payments = relationship(
        "HRPayment",
        primaryjoin="and_(PermanentStaff.id==foreign(HRPayment.staff_id), "
                    "HRPayment.worker_type=='permanent')",
        viewonly=True
    )

    work_sessions = relationship(
        "HRWorkSession",
        primaryjoin="and_(PermanentStaff.id==foreign(HRWorkSession.staff_id), "
                    "HRWorkSession.worker_type=='permanent')",
        viewonly=True
    )

    payrolls = relationship("Payroll", back_populates="employee")

    finance_entries = relationship(
        "FinanceHR",
        viewonly=True,
        primaryjoin="PermanentStaff.id==foreign(FinanceHR.staff_id)"
    )


# ============================================================
# CASUAL WORKER
# ============================================================
class CasualWorker(Base):
    __tablename__ = "casual_workers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False, index=True)
    module_type = Column(String(50), nullable=False, default="mixed")

    name = Column(String(255), nullable=False)
    contact = Column(String(100))
    daily_rate = Column(Float, default=0.0)

    total_days_worked = Column(Integer, default=0)
    total_pay = Column(Float, default=0.0)
    status = Column(String(50), default="active")

    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouses.id"), nullable=True)
    skill = Column(String(100))

    is_active = Column(Boolean, default=True)
    deleted_at = Column(Date, nullable=True)

    created_at = Column(Date, default=datetime.date.today)
    updated_at = Column(Date, default=datetime.date.today, onupdate=datetime.date.today)

    # Relationships
    payments = relationship(
        "HRPayment",
        primaryjoin="and_(CasualWorker.id==foreign(HRPayment.staff_id), "
                    "HRPayment.worker_type=='casual')",
        viewonly=True
    )

    work_sessions = relationship(
        "HRWorkSession",
        primaryjoin="and_(CasualWorker.id==foreign(HRWorkSession.staff_id), "
                    "HRWorkSession.worker_type=='casual')",
        viewonly=True
    )

    finance_entries = relationship(
        "FinanceHR",
        viewonly=True,
        primaryjoin="CasualWorker.id==foreign(FinanceHR.staff_id)"
    )


# ============================================================
# HR WORK SESSION  (✅ CROP INTEGRATED)
# ============================================================
class HRWorkSession(Base):
    __tablename__ = "hr_work_sessions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    staff_id = Column(Integer, nullable=False, index=True)
    worker_type = Column(String(20), nullable=False)  # permanent | casual
    module_type = Column(String(50), default="crop")

    date = Column(Date, default=datetime.date.today)
    activity = Column(String(100), nullable=False)
    task_description = Column(Text)

    hours_worked = Column(Float, default=0.0)
    wage_rate = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)

    # 🔗 Crop linkage (FINAL ADDITION)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=True)
    activity_id = Column(Integer, nullable=True)

    farm_id = Column(Integer, ForeignKey("farms.id"), index=True)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouses.id"), nullable=True)

    status = Column(String(50), default="pending")

    is_active = Column(Boolean, default=True)
    deleted_at = Column(Date, nullable=True)

    created_at = Column(Date, default=datetime.date.today)
    updated_at = Column(Date, default=datetime.date.today, onupdate=datetime.date.today)

    permanent_staff = relationship(
        "PermanentStaff",
        primaryjoin="and_(PermanentStaff.id==foreign(HRWorkSession.staff_id), "
                    "HRWorkSession.worker_type=='permanent')",
        viewonly=True
    )

    casual_worker = relationship(
        "CasualWorker",
        primaryjoin="and_(CasualWorker.id==foreign(HRWorkSession.staff_id), "
                    "HRWorkSession.worker_type=='casual')",
        viewonly=True
    )

    finance_entry = relationship(
        "FinanceHR",
        viewonly=True,
        primaryjoin="HRWorkSession.id==foreign(FinanceHR.work_session_id)"
    )


# ============================================================
# HR PAYMENT
# ============================================================
class HRPayment(Base):
    __tablename__ = "hr_payments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    staff_id = Column(Integer, nullable=False, index=True)
    worker_type = Column(String(20), nullable=False)
    module_type = Column(String(50), default="mixed")

    amount = Column(Float, default=0.0)
    description = Column(Text)
    payment_method = Column(String(50))
    payment_date = Column(Date, default=datetime.date.today)
    status = Column(String(50), default="completed")

    farm_id = Column(Integer, ForeignKey("farms.id"), index=True)

    is_active = Column(Boolean, default=True)
    deleted_at = Column(Date, nullable=True)

    created_at = Column(Date, default=datetime.date.today)
    updated_at = Column(Date, default=datetime.date.today, onupdate=datetime.date.today)

    permanent_staff = relationship(
        "PermanentStaff",
        primaryjoin="and_(PermanentStaff.id==foreign(HRPayment.staff_id), "
                    "HRPayment.worker_type=='permanent')",
        viewonly=True
    )

    casual_worker = relationship(
        "CasualWorker",
        primaryjoin="and_(CasualWorker.id==foreign(HRPayment.staff_id), "
                    "HRPayment.worker_type=='casual')",
        viewonly=True
    )

    finance_entry = relationship(
        "FinanceHR",
        viewonly=True,
        primaryjoin="HRPayment.id==foreign(FinanceHR.payment_id)"
    )


# ============================================================
# PAYROLL (Permanent Staff Only)
# ============================================================
class Payroll(Base):
    __tablename__ = "payroll"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("permanent_staff.id"), nullable=False)

    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)

    gross_pay = Column(Float, default=0.0)
    deductions = Column(Float, default=0.0)
    net_pay = Column(Float, default=0.0)

    paid_on = Column(Date)
    payment_method = Column(String(50))
    reference = Column(String(100), unique=True, index=True)
    recorded_by = Column(String(100), default="system")

    is_active = Column(Boolean, default=True)
    deleted_at = Column(Date)

    created_at = Column(Date, default=datetime.date.today)
    updated_at = Column(Date, default=datetime.date.today, onupdate=datetime.date.today)

    employee = relationship("PermanentStaff", back_populates="payrolls")


