#backend/core/dependencies.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.modules.farms.models import Farm
from backend.modules.users.models import User, FarmMember
                                                                                                            

def get_current_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Farm:
    farm = (
        db.query(Farm)
        .filter(
            Farm.id == farm_id,
            Farm.owner_id == current_user.id
        )
        .first()
    )

    if not farm:
        raise HTTPException(status_code=403, detail="Farm not found or access denied")

    return farm


def get_current_farm(farm_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Farm:
    membership = db.query(FarmMember).filter(
        FarmMember.farm_id == farm_id,
        FarmMember.user_id == current_user.id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied to this farm")
    return membership.farm

