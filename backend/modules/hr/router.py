# backend/modules/hr/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from backend.core.database import get_db
from backend.modules.hr import services as service
from backend.modules.hr import schemas

router = APIRouter(tags=["HR"])

# ============================================================
# 👷 Permanent Staff
# ============================================================
@router.post("/permanent/add", response_model=schemas.PermanentStaffResponse)
def add_permanent_staff(
    request: schemas.PermanentStaffCreate, db: Session = Depends(get_db)
):
    try:
        return service.create_permanent_staff(db, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/permanent/list", response_model=List[schemas.PermanentStaffResponse])
def list_permanent_staff(farm_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return service.list_permanent_staff(db, farm_id=farm_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/permanent/{staff_id}", response_model=schemas.PermanentStaffResponse)
def update_permanent_staff(staff_id: int, request: schemas.PermanentStaffCreate, db: Session = Depends(get_db)):
    staff = service.update_permanent_staff(db, staff_id, request)
    if not staff:
        raise HTTPException(status_code=404, detail="Permanent staff not found")
    return staff


@router.delete("/permanent/{staff_id}")
def deactivate_permanent_staff(staff_id: int, db: Session = Depends(get_db)):
    success = service.deactivate_permanent_staff(db, staff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permanent staff not found")
    return {"detail": "Permanent staff deactivated"}


# ============================================================
# 👷 Casual Worker
# ============================================================
@router.post("/casual/add", response_model=schemas.CasualWorkerResponse)
def add_casual_worker(request: schemas.CasualWorkerCreate, db: Session = Depends(get_db)):
    try:
        return service.create_casual_worker(db, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/casual/list", response_model=List[schemas.CasualWorkerResponse])
def list_casual_workers(farm_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return service.list_casual_workers(db, farm_id=farm_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/casual/{worker_id}", response_model=schemas.CasualWorkerResponse)
def update_casual_worker(worker_id: int, request: schemas.CasualWorkerCreate, db: Session = Depends(get_db)):
    worker = service.update_casual_worker(db, worker_id, request)
    if not worker:
        raise HTTPException(status_code=404, detail="Casual worker not found")
    return worker


@router.delete("/casual/{worker_id}")
def deactivate_casual_worker(worker_id: int, db: Session = Depends(get_db)):
    success = service.deactivate_casual_worker(db, worker_id)
    if not success:
        raise HTTPException(status_code=404, detail="Casual worker not found")
    return {"detail": "Casual worker deactivated"}


# ============================================================
# 🧾 Work Session
# ============================================================
@router.post("/work-session", response_model=schemas.HRWorkSessionResponse)
def record_work_session(request: schemas.HRWorkSessionCreate, db: Session = Depends(get_db)):
    try:
        return service.create_work_session(db, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/work-session/list", response_model=List[schemas.HRWorkSessionResponse])
def list_work_sessions(staff_id: Optional[int] = None, worker_type: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        return service.list_work_sessions(db, staff_id=staff_id, worker_type=worker_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# 💵 HR Payment
# ============================================================
@router.post("/payment", response_model=schemas.HRPaymentResponse)
def record_payment(request: schemas.HRPaymentCreate, db: Session = Depends(get_db)):
    try:
        return service.create_payment(db, request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/payment/list", response_model=List[schemas.HRPaymentResponse])
def list_payments(staff_id: Optional[int] = None, worker_type: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        return service.list_payments(db, staff_id=staff_id, worker_type=worker_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# 📅 Payroll
# ============================================================
@router.post("/payroll/generate/{employee_id}", response_model=schemas.PayrollResponse)
def generate_payroll(employee_id: int, period_start: date, period_end: date, db: Session = Depends(get_db)):
    try:
        return service.create_payroll(
            db,
            schemas.PayrollCreate(employee_id=employee_id, period_start=period_start, period_end=period_end)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/payroll/list", response_model=List[schemas.PayrollResponse])
def list_payrolls(employee_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return service.list_payrolls(db, employee_id=employee_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# 📤 EXPORT ROUTES (PDF & Excel)
# ============================================================
from backend.modules.hr.report_export_router import router as export_router
router.include_router(export_router, prefix="/export", tags=["HR Export"])
