#backend/modules/finance/models.py

from datetime import date, datetime
from sqlalchemy import (
    Column, Integer, String, Float, Date, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.types import Enum as SQLEnum
from backend.core.database import Base
from sqlalchemy import JSON

from enum import Enum

# ============================================================
# MODULE TYPES ENUM
# ============================================================
class ModuleType(str, Enum):
    CROP = "crop"
    LIVESTOCK = "livestock"
    POULTRY = "poultry"
    AQUACULTURE = "aquaculture"
    HR = "hr"
    STORE = "store"
    GENERAL = "general"


# ============================================================
# UNIVERSAL FINANCE BASE
# ============================================================
class FinanceBase(Base):
    __tablename__ = "finance_base"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)  # income | expense
    source = Column(String, default="Manual Entry")
    date = Column(Date, default=date.today)

    receipt_file = Column(String, nullable=True)
    uploaded_by = Column(String, nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)

    module_type = Column(SQLEnum(ModuleType), nullable=False)

    linked_entity_id = Column(Integer, nullable=True)  
    # e.g. activity_id, payroll_id, sale_id, store_transaction_id

    # Relationships
    farm = relationship("Farm", backref="finance_entries")

    # One-to-one module sub-records
    crop_details = relationship("FinanceCrop", back_populates="base", uselist=False)
    livestock_details = relationship("FinanceLivestock", back_populates="base", uselist=False)
    poultry_details = relationship("FinancePoultry", back_populates="base", uselist=False)
    aquaculture_details = relationship("FinanceAquaculture", back_populates="base", uselist=False)
    hr_details = relationship("FinanceHR", back_populates="base", uselist=False)
    store_details = relationship("FinanceInventory", back_populates="base", uselist=False)


# ============================================================
# HR FINANCE
# ============================================================
class FinanceHR(Base):
    __tablename__ = "finance_hr"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    base_id = Column(Integer, ForeignKey("finance_base.id"), nullable=False)

    # Polymorphic worker link
    staff_id = Column(Integer, nullable=False)  
    worker_type = Column(String(20), nullable=False)  # permanent | casual

    # Optional financial links
    payment_id = Column(Integer, nullable=True)
    work_session_id = Column(Integer, nullable=True)
    reference_id = Column(Integer, nullable=True)

    # Parent link
    base = relationship("FinanceBase", back_populates="hr_details")

    # --------------------------------------------------------
    # Relationships (view-only, dynamic)
    # --------------------------------------------------------

    # Permanent staff
    permanent_staff = relationship(
        "backend.modules.hr.models.PermanentStaff",
        primaryjoin="PermanentStaff.id==foreign(FinanceHR.staff_id)",
        viewonly=True
    )

    # Casual staff
    casual_staff = relationship(
        "backend.modules.hr.models.CasualWorker",
        primaryjoin="CasualWorker.id==foreign(FinanceHR.staff_id)",
        viewonly=True
    )

    # Polymorphic shortcut (HR models reference this as back_populates="staff")
    staff = relationship(
        "backend.modules.hr.models.PermanentStaff",
        primaryjoin="PermanentStaff.id==foreign(FinanceHR.staff_id)",
        viewonly=True
    )

    payment = relationship(
        "backend.modules.hr.models.HRPayment",
        primaryjoin="HRPayment.id==foreign(FinanceHR.payment_id)",
        viewonly=True
    )

    work_session = relationship(
        "backend.modules.hr.models.HRWorkSession",
        primaryjoin="HRWorkSession.id==foreign(FinanceHR.work_session_id)",
        viewonly=True
    )



# ============================================================
# STORE / INVENTORY FINANCE
# ============================================================
class FinanceInventory(Base):
    __tablename__ = "finance_inventory"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    base_id = Column(Integer, ForeignKey("finance_base.id"), nullable=False)
    transaction_id = Column(Integer, nullable=False)
    # Example: inventory_out, inventory_in, purchase order, request

    base = relationship("FinanceBase", back_populates="store_details")


# ============================================================
# CROP FINANCE
# ============================================================
class FinanceCrop(Base):
    __tablename__ = "finance_crop"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    base_id = Column(Integer, ForeignKey("finance_base.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)

    base = relationship("FinanceBase", back_populates="crop_details")
    crop = relationship("Crop", backref="finance_entries")
    block = relationship("Block", backref="finance_entries")


# ============================================================
# LIVESTOCK FINANCE
# ============================================================
class FinanceLivestock(Base):
    __tablename__ = "finance_livestock"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    base_id = Column(Integer, ForeignKey("finance_base.id"), nullable=False)
    livestock_id = Column(Integer, ForeignKey("livestock.id"), nullable=False)

    reference_id = Column(Integer, nullable=True)

    base = relationship("FinanceBase", back_populates="livestock_details")
    livestock = relationship("Livestock", backref="finance_entries")


# ============================================================
# POULTRY FINANCE
# ============================================================
class FinancePoultry(Base):
    __tablename__ = "finance_poultry"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    base_id = Column(Integer, ForeignKey("finance_base.id"), nullable=False)
    poultry_id = Column(Integer, ForeignKey("poultry_batches.id"), nullable=False)

    reference_id = Column(Integer, nullable=True)

    base = relationship("FinanceBase", back_populates="poultry_details")
    poultry = relationship("PoultryBatch", backref="finance_entries")


# ============================================================
# AQUACULTURE FINANCE
# ============================================================
class FinanceAquaculture(Base):
    __tablename__ = "finance_aquaculture"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    base_id = Column(Integer, ForeignKey("finance_base.id"), nullable=False)
    aquaculture_id = Column(Integer, ForeignKey("aquaculture.id"), nullable=False)

    reference_id = Column(Integer, nullable=True)

    base = relationship("FinanceBase", back_populates="aquaculture_details")
    aquaculture = relationship("Aquaculture", backref="finance_entries")


# ============================================================
# PROFIT & LOSS
# ============================================================
class ProfitLoss(Base):
    __tablename__ = "profit_loss"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    total_income = Column(Float, default=0.0)
    total_expense = Column(Float, default=0.0)
    net_profit = Column(Float, default=0.0)

    farm = relationship("Farm", backref="profit_loss")


# ============================================================
# INVOICE
# ============================================================
class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)

    date_issued = Column(Date, default=date.today)
    due_date = Column(Date, nullable=True)
    status = Column(String, default="unpaid")

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)

    farm = relationship("Farm", backref="invoices")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")


# ============================================================
# PAYMENT
# ============================================================
class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    payment_reference = Column(String, nullable=False, unique=True)
    amount = Column(Float, nullable=False)
    date_paid = Column(Date, default=date.today)
    method = Column(String, default="cash")

    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)

    invoice = relationship("Invoice", back_populates="payments")
    farm = relationship("Farm", backref="payments")



# ============================================================
# FARM MODULE SUBSCRIPTION
# ============================================================

class FarmModuleSubscription(Base):
    __tablename__ = "farm_module_subscriptions"
    __table_args__ = {"extend_existing": True}    

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    module_type = Column(SQLEnum(ModuleType), nullable=False)
    is_active = Column(Boolean, default=True)
    subscribed_on = Column(DateTime, default=datetime.utcnow)
