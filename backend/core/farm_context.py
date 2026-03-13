from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.modules.farms.models import Farm, FarmMember


def get_current_farm(
    x_farm_id: int | None = Header(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Resolves the active farm from X-Farm-ID header.
    Ensures the user owns or is a member of the farm.
    """

    if not x_farm_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Farm-ID header is required",
        )

    farm = db.query(Farm).filter(Farm.id == x_farm_id).first()

    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )

    # Owner always allowed
    if farm.owner_id == current_user.id:
        return farm

    # Check membership
    member = (
        db.query(FarmMember)
        .filter(
            FarmMember.farm_id == farm.id,
            FarmMember.user_id == current_user.id,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this farm",
        )

    return farm

