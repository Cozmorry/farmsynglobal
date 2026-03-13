# backend/modules/auth/router.py
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_

from fastapi import APIRouter, Depends, HTTPException, status, Request

from backend.core.database import get_db
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user,
)
from backend.modules.users.models import User
from backend.modules.auth.schemas import LoginSchema, RegisterSchema
from backend.core.limiter import limiter

router = APIRouter(tags=["Auth"])

# ============================================================
# LOGIN (RATE LIMITED)
# ============================================================

@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    payload: LoginSchema,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        or_(
            User.username == payload.identifier,
            User.email == payload.identifier
        )
    ).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.id)}

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )

    # ============================================================
    # Build farm list with active modules
    # ============================================================
    farm_list = []

    # Owned farms
    for farm in user.owned_farms:
        farm_list.append({
            "id": farm.id,
            "name": farm.name,
            "role": "owner",
            "active_modules": farm.active_modules or []
        })

    # Membership farms
    for membership in user.farm_memberships:
        if membership.farm_id not in [f["id"] for f in farm_list]:
            farm_list.append({
                "id": membership.farm.id,
                "name": membership.farm.name,
                "role": membership.role.value,
                "active_modules": membership.farm.active_modules or []
            })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "farms": farm_list
        }
    }

# ============================================================
# REGISTER (RATE LIMITED + MASS-ASSIGNMENT SAFE)
# ============================================================

@router.post("/register")
@limiter.limit("10/minute")
def register(
    request: Request,
    payload: RegisterSchema,
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password),
        is_active=True,
        is_superuser=False,  # 🔒 forced
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "farms": []
    }

# ============================================================
# CURRENT USER
# ============================================================

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    farm_list = []

    # Owned farms
    for farm in current_user.owned_farms:
        farm_list.append({
            "id": farm.id,
            "name": farm.name,
            "role": "owner",
            "active_modules": farm.active_modules or []
        })

    # Membership farms
    for membership in current_user.farm_memberships:
        if membership.farm_id not in [f["id"] for f in farm_list]:
            farm_list.append({
                "id": membership.farm.id,
                "name": membership.farm.name,
                "role": membership.role.value,
                "active_modules": membership.farm.active_modules or []
            })

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "farms": farm_list
    }
