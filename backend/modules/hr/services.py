# modules/hr/services.py
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from backend.modules.hr import models, schemas


# ============================================================
# Permanent Staff Services
# ============================================================
def create_permanent_staff(db: Session, staff_in: schemas.PermanentStaffCreate) -> models.PermanentStaff:
    staff = models.PermanentStaff(**staff_in.dict())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


def get_permanent_staff(db: Session, staff_id: int) -> Optional[models.PermanentStaff]:
    return db.query(models.PermanentStaff).filter(models.PermanentStaff.id == staff_id, models.PermanentStaff.is_active == True).first()


def list_permanent_staff(db: Session, farm_id: Optional[int] = None) -> List[models.PermanentStaff]:
    query = db.query(models.PermanentStaff).filter(models.PermanentStaff.is_active == True)
    if farm_id:
        query = query.filter(models.PermanentStaff.farm_id == farm_id)
    return query.all()


def update_permanent_staff(db: Session, staff_id: int, staff_in: schemas.PermanentStaffCreate) -> Optional[models.PermanentStaff]:
    staff = get_permanent_staff(db, staff_id)
    if not staff:
        return None
    for field, value in staff_in.dict(exclude_unset=True).items():
        setattr(staff, field, value)
    db.commit()
    db.refresh(staff)
    return staff


def deactivate_permanent_staff(db: Session, staff_id: int) -> bool:
    staff = get_permanent_staff(db, staff_id)
    if not staff:
        return False
    staff.is_active = False
    staff.deleted_at = date.today()
    db.commit()
    return True


# ============================================================
# Casual Worker Services
# ============================================================
def create_casual_worker(db: Session, worker_in: schemas.CasualWorkerCreate) -> models.CasualWorker:
    worker = models.CasualWorker(**worker_in.dict())
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker


def get_casual_worker(db: Session, worker_id: int) -> Optional[models.CasualWorker]:
    return db.query(models.CasualWorker).filter(models.CasualWorker.id == worker_id, models.CasualWorker.is_active == True).first()


def list_casual_workers(db: Session, farm_id: Optional[int] = None) -> List[models.CasualWorker]:
    query = db.query(models.CasualWorker).filter(models.CasualWorker.is_active == True)
    if farm_id:
        query = query.filter(models.CasualWorker.farm_id == farm_id)
    return query.all()


def update_casual_worker(db: Session, worker_id: int, worker_in: schemas.CasualWorkerCreate) -> Optional[models.CasualWorker]:
    worker = get_casual_worker(db, worker_id)
    if not worker:
        return None
    for field, value in worker_in.dict(exclude_unset=True).items():
        setattr(worker, field, value)
    db.commit()
    db.refresh(worker)
    return worker


def deactivate_casual_worker(db: Session, worker_id: int) -> bool:
    worker = get_casual_worker(db, worker_id)
    if not worker:
        return False
    worker.is_active = False
    worker.deleted_at = date.today()
    db.commit()
    return True


# ============================================================
# HR Work Session Services
# ============================================================
def create_work_session(db: Session, session_in: schemas.HRWorkSessionCreate) -> models.HRWorkSession:
    session_obj = models.HRWorkSession(**session_in.dict())
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj


def get_work_session(db: Session, session_id: int) -> Optional[models.HRWorkSession]:
    return db.query(models.HRWorkSession).filter(models.HRWorkSession.id == session_id, models.HRWorkSession.is_active == True).first()


def list_work_sessions(db: Session, staff_id: Optional[int] = None, worker_type: Optional[str] = None) -> List[models.HRWorkSession]:
    query = db.query(models.HRWorkSession).filter(models.HRWorkSession.is_active == True)
    if staff_id:
        query = query.filter(models.HRWorkSession.staff_id == staff_id)
    if worker_type:
        query = query.filter(models.HRWorkSession.worker_type == worker_type)
    return query.all()


# ============================================================
# HR Payment Services
# ============================================================
def create_payment(db: Session, payment_in: schemas.HRPaymentCreate) -> models.HRPayment:
    payment = models.HRPayment(**payment_in.dict())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, payment_id: int) -> Optional[models.HRPayment]:
    return db.query(models.HRPayment).filter(models.HRPayment.id == payment_id, models.HRPayment.is_active == True).first()


def list_payments(db: Session, staff_id: Optional[int] = None, worker_type: Optional[str] = None) -> List[models.HRPayment]:
    query = db.query(models.HRPayment).filter(models.HRPayment.is_active == True)
    if staff_id:
        query = query.filter(models.HRPayment.staff_id == staff_id)
    if worker_type:
        query = query.filter(models.HRPayment.worker_type == worker_type)
    return query.all()


# ============================================================
# Payroll Services
# ============================================================
def create_payroll(db: Session, payroll_in: schemas.PayrollCreate) -> models.Payroll:
    payroll = models.Payroll(**payroll_in.dict())
    db.add(payroll)
    db.commit()
    db.refresh(payroll)
    return payroll


def get_payroll(db: Session, payroll_id: int) -> Optional[models.Payroll]:
    return db.query(models.Payroll).filter(models.Payroll.id == payroll_id, models.Payroll.is_active == True).first()


def list_payrolls(db: Session, employee_id: Optional[int] = None) -> List[models.Payroll]:
    query = db.query(models.Payroll).filter(models.Payroll.is_active == True)
    if employee_id:
        query = query.filter(models.Payroll.employee_id == employee_id)
    return query.all()
