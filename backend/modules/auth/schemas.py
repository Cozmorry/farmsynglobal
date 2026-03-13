# backend/modules/auth/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List
from enum import Enum


# ============================================================
# LOGIN
# ============================================================

class LoginSchema(BaseModel):
    identifier: str
    password: str

    class Config:
        extra = "forbid"


# ============================================================
# REGISTER
# ============================================================

class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        extra = "forbid"


# ============================================================
# FARM (embedded in user response)
# ============================================================

class FarmRoleEnum(str, Enum):
    owner = "owner"
    manager = "manager"
    worker = "worker"
    vet = "vet"
    accountant = "accountant"

class UserFarm(BaseModel):
    id: int
    name: str
    role: FarmRoleEnum

    class Config:
        orm_mode = True


# ============================================================
# USER RESPONSE
# ============================================================

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    farms: List[UserFarm] = []

    class Config:
        orm_mode = True

