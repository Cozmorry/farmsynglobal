# backend/identity/tenants/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.core.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    address = Column(String(500), nullable=True)
    phone_number = Column(String(50), nullable=True)
    selected_modules = Column(JSON, default=list)  # MySQL/SQLite compatible; PostgreSQL ARRAY alternative

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="owned_tenants")
    farms = relationship("Farm", back_populates="tenant", cascade="all, delete-orphan")
