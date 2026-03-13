# backend/modules/tenants/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List

class TenantCreate(BaseModel):
    name: str
    email: EmailStr
    address: str | None = None
    phone_number: str | None = None
    selected_modules: List[str] = []

class TenantRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: str | None
    phone_number: str | None
    selected_modules: List[str]

    class Config:
        from_attributes = True  # Pydantic v2 ORM mode
