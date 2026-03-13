# backend/modules/users/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from backend.modules.farms.schemas import FarmRoleEnum


# ----------------------------
# USER SCHEMAS
# ----------------------------

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


# ----------------------------
# FARM MEMBER SCHEMAS
# ----------------------------

class FarmMemberCreate(BaseModel):
    user_id: int
    role: FarmRoleEnum

class FarmMemberOut(BaseModel):
    id: int
    user_id: int
    farm_id: int
    role: FarmRoleEnum

    class Config:
        orm_mode = True

