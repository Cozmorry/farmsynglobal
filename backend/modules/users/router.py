# backend/modules/users/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.modules.users.schemas import UserOut, FarmMemberCreate, FarmMemberOut
from backend.modules.users.services import get_user_by_email, add_user_to_farm
from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.modules.users.models import User
from backend.modules.farms.models import FarmMember
from backend.modules.farms.models import Farm

router = APIRouter(tags=["Users"])

# -------------------------------
# GET USER
# -------------------------------
@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Allow self or superuser only
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user



# -------------------------------
# ASSIGN USER TO FARM
# -------------------------------
@router.post("/farms/{farm_id}/members", response_model=FarmMemberOut)
def assign_user_to_farm(
    farm_id: int,
    payload: FarmMemberCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 🔐 SECURITY: only farm owner can assign members
    farm = (
        db.query(Farm)
        .filter(Farm.id == farm_id, Farm.owner_id == current_user.id)
        .first()
    )

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the farm owner can assign members"
        )

    membership = add_user_to_farm(
        db,
        user_id=payload.user_id,
        farm_id=farm_id,
        role=payload.role.value,
    )
    return membership


# -------------------------------
# LIST USERS (for farm member selection)
# -------------------------------
@router.get("", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Optional: restrict to superuser only
    # if not current_user.is_superuser:
    #     raise HTTPException(status_code=403, detail="Access denied")

    return db.query(User).all()
