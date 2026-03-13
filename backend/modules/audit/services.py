#backend/modules/audit/services.py

from sqlalchemy.orm import Session
from .models import AuditLog


def log_action(
    db: Session,
    *,
    user_id: int,
    action: str,
    resource: str,
    resource_id: int | None = None,
    farm_id: int | None = None,
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        farm_id=farm_id,
    )
    db.add(log)
    db.commit()
