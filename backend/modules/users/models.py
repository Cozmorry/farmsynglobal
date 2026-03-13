# backend/modules/users/models.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import JSON


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(512), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # --------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------

    # Farms owned by this user
    owned_farms = relationship(
        "Farm",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # Farm memberships (manager, worker, vet, etc.)
    farm_memberships = relationship(
        "FarmMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    owned_tenants = relationship("Tenant", back_populates="owner")


