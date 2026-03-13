# backend/modules/tenants/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from . import schemas, services

router = APIRouter(tags=["Tenants"])

# Create tenant
@router.post("/create", response_model=schemas.TenantRead)
def create_tenant_basic(payload: schemas.TenantCreate, db: Session = Depends(get_db)):
    return services.create_tenant(db, payload)

# Assign modules
@router.put("/{tenant_id}/modules", response_model=schemas.TenantRead)
def assign_modules(tenant_id: int, modules: list[str], db: Session = Depends(get_db)):
    tenant = services.get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    tenant.selected_modules = modules
    db.commit()
    db.refresh(tenant)
    return tenant

# Get all tenants
@router.get("/", response_model=list[schemas.TenantRead])
def get_all_tenants(db: Session = Depends(get_db)):
    return services.list_tenants(db)
