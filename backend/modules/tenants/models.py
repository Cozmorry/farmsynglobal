# backend/identity/tenants/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY  # Use JSON for SQLite
from backend.core.database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    selected_modules = Column(ARRAY(String), default=[])  # Use JSON for SQLite: Column(JSON, default=[])

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="owned_tenants")
    farms = relationship("Farm", back_populates="tenant", cascade="all, delete-orphan")
