# backend/core/module_guard.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.modules.farms.models import Farm
from backend.modules.users.models import User


def require_module(module_name: str):
    """
    Dependency factory that ensures a module is active for a given farm.
    """

    def module_checker(
        farm_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        # Get farm
        farm = db.query(Farm).filter(Farm.id == farm_id).first()

        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")

        # 🔐 Ensure user belongs to farm (owner or member)
        is_owner = farm.owner_id == current_user.id
        is_member = any(
            member.user_id == current_user.id
            for member in farm.members
        )

        if not is_owner and not is_member:
            raise HTTPException(
                status_code=403,
                detail="Access denied to this farm",
            )

        # 🚨 Check if module is active
        if module_name not in farm.active_modules:
            raise HTTPException(
                status_code=403,
                detail=f"{module_name} module not active for this farm",
            )

        return farm

    return module_checker
