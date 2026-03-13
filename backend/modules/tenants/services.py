# backend/modules/tenants/services.py
from sqlalchemy.orm import Session
from . import models, schemas

def create_tenant(db: Session, payload: schemas.TenantCreate) -> models.Tenant:
    data = payload.model_dump()
    tenant = models.Tenant(**data)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

def get_tenant(db: Session, tenant_id: int) -> models.Tenant | None:
    return db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()

def list_tenants(db: Session) -> list[models.Tenant]:
    return db.query(models.Tenant).all()
