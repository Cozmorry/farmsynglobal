#backend/modules/poultry/models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import date
from backend.core.database import Base
from sqlalchemy import JSON

# ============================================================
# 🐔 Poultry Batches (Main flock)
# ============================================================
class PoultryBatch(Base):
    __tablename__ = "poultry_batches"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    batch_name = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    batch_size = Column(Integer, nullable=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    start_date = Column(Date, default=date.today)
    housing_type = Column(String, nullable=True)
    purpose = Column(String, nullable=True)
    source = Column(String, nullable=True)
    expected_cycle_days = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String, default="Active")

    # Relationships
    activities = relationship(
        "PoultryActivity", back_populates="batch", cascade="all, delete-orphan"
    )
    productions = relationship(
        "PoultryProduction", back_populates="batch", cascade="all, delete-orphan"
    )
    sales = relationship(
        "PoultrySale", back_populates="batch", cascade="all, delete-orphan"
    )

    # Veterinary health records (separate module)
    health_records = relationship(
        "PoultryHealth", back_populates="batch", cascade="all, delete-orphan"
    )


# ============================================================
# 🧾 Poultry Activities (Daily logs)
# ============================================================
class PoultryActivity(Base):
    __tablename__ = "poultry_activities"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    poultry_batch_id = Column(Integer, ForeignKey("poultry_batches.id"))
    date = Column(Date, default=date.today)

    activity_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    performed_by = Column(String, nullable=True)

    # Quantities ONLY
    feed_used_kg = Column(Float, nullable=True)
    water_used_l = Column(Float, nullable=True)
    drugs_used_qty = Column(Float, nullable=True)
    mortality = Column(Integer, default=0)

    # HARD LINKS (cost origin)
    inventory_transaction_id = Column(Integer, nullable=True)
    hr_work_session_id = Column(Integer, nullable=True)

    # Environment
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    batch = relationship("PoultryBatch", back_populates="activities")


# ============================================================
# 🥚 Poultry Production (Eggs / Meat / Chicks)
# ============================================================
class PoultryProduction(Base):
    __tablename__ = "poultry_production"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    poultry_batch_id = Column(Integer, ForeignKey("poultry_batches.id"))
    production_type = Column(String, nullable=False)
    date = Column(Date, default=date.today)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, default=0.0)
    quality_grade = Column(String, nullable=True)
    remarks = Column(Text, nullable=True)

    batch = relationship("PoultryBatch", back_populates="productions")


# ============================================================
# 💵 Poultry Sales
# ============================================================
class PoultrySale(Base):
    __tablename__ = "poultry_sales"

    id = Column(Integer, primary_key=True, index=True)
    poultry_batch_id = Column(Integer, ForeignKey("poultry_batches.id"))
    sale_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    sale_date = Column(Date, default=date.today)
    buyer_name = Column(String, nullable=True)
    payment_status = Column(String, default="Pending")

    batch = relationship("PoultryBatch", back_populates="sales")

    @property
    def total_amount(self):
        return (self.quantity or 0) * (self.unit_price or 0)
