# backend/modules/farms/models.py

# backend/modules/farms/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum
from backend.core.database import Base
from backend.modules.users.models import User


import enum


# ============================================================
# ENUMS
# ============================================================

class FarmRoleEnum(str, enum.Enum):
    owner = "owner"
    manager = "manager"
    worker = "worker"
    vet = "vet"
    accountant = "accountant"


class FarmTypeEnum(str, enum.Enum):
    crop = "crop"
    livestock = "livestock"
    poultry = "poultry"
    aquaculture = "aquaculture"
    mixed = "mixed"


# ============================================================
# FARM
# ============================================================

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=False)

    farm_type = Column(
        SqlEnum(FarmTypeEnum, name="farm_type_enum"),
        nullable=False,
        default=FarmTypeEnum.mixed,
    )

    # ✅ SAFE JSON DEFAULTS
    size = Column(
        JSON,
        nullable=False,
        default=lambda: {"value": 0.0, "unit": "ha"},
    )

    active_modules = Column(
        JSON,
        nullable=False,
        default=list,
    )

    scale = Column(String(50), nullable=False, default="small")  # "small", "medium", "large"
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # ---------------- RELATIONSHIPS ----------------
    owner = relationship("User", back_populates="owned_farms")
    members = relationship(
        "FarmMember",
        back_populates="farm",
        cascade="all, delete-orphan"
    )
    blocks = relationship(
        "Block",
        back_populates="farm",
        cascade="all, delete-orphan"
    )
    greenhouses = relationship(
        "Greenhouse",
        back_populates="farm",
        cascade="all, delete-orphan"
    )
    barns = relationship(
        "Barn",
        back_populates="farm",
        cascade="all, delete-orphan"
    )
    coops = relationship(
        "Coop",
        back_populates="farm",
        cascade="all, delete-orphan"
    )
    ponds = relationship(
        "Pond",
        back_populates="farm",
        cascade="all, delete-orphan"
    )
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    tenant = relationship("Tenant", back_populates="farms")
        
        

# ============================================================
# FARM MEMBER
# ============================================================

class FarmMember(Base):
    __tablename__ = "farm_members"

    __table_args__ = (
        UniqueConstraint("farm_id", "user_id", name="uq_farm_user"),
    )

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(
        Integer,
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    role = Column(SqlEnum(FarmRoleEnum), nullable=False)

    farm = relationship("Farm", back_populates="members")
    user = relationship("User", back_populates="farm_memberships")


# ============================================================
# BLOCK
# ============================================================

class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    area = Column(
        JSON,
        nullable=False,
        default=lambda: {"value": 0.0, "unit": "ha"},
    )

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)

    farm = relationship("Farm", back_populates="blocks")
    greenhouses = relationship(
        "Greenhouse",
        back_populates="block",
        cascade="all, delete-orphan"
    )


# ============================================================
# GREENHOUSE
# ============================================================

class Greenhouse(Base):
    __tablename__ = "greenhouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    area = Column(
        JSON,
        nullable=False,
        default=lambda: {"value": 0.0, "unit": "ha"},
    )

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=True)

    farm = relationship("Farm", back_populates="greenhouses")
    block = relationship("Block", back_populates="greenhouses")


# ============================================================
# BARN
# ============================================================

class Barn(Base):
    __tablename__ = "barns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    capacity = Column(Integer)

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)

    farm = relationship("Farm", back_populates="barns")


# ============================================================
# COOP
# ============================================================

class Coop(Base):
    __tablename__ = "coops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    capacity = Column(Integer)

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)

    farm = relationship("Farm", back_populates="coops")


# ============================================================
# POND
# ============================================================

class Pond(Base):
    __tablename__ = "ponds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    size = Column(
        JSON,
        nullable=False,
        default=lambda: {"value": 0.0, "unit": "ha"},
    )

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)

    farm = relationship("Farm", back_populates="ponds")
