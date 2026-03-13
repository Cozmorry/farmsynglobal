#backend/modules/finance/router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from fastapi.responses import StreamingResponse

from backend.core.database import get_db
from backend.modules.finance.schemas import (
    FinancialSummary,
    InvoiceSchema,
    InvoiceCreate,
    PaymentSchema,
    PaymentCreate,
    BaseFinanceEntryCreate,
    BaseFinanceEntrySchema,
)
from backend.modules.finance.models import ModuleType
from backend.modules.finance.services import FinanceService
from backend.modules.finance.finance_report_service import FinanceReportService

router = APIRouter(tags=["Finance"],)

# ===========================================================
# FINANCE ENTRY ENDPOINTS
# ===========================================================

@router.post("/entries", response_model=BaseFinanceEntrySchema)
def create_finance_entry(
    request: BaseFinanceEntryCreate,
    db: Session = Depends(get_db),
):
    """
    Creates a finance entry.
    NOTE:
    Production-linked finance entries should ideally be created
    automatically from their respective modules.
    """
    service = FinanceService(db)
    return service.create_finance_entry(request.dict())


@router.get("/entries/{entry_id}", response_model=BaseFinanceEntrySchema)
def get_finance_entry(entry_id: int, db: Session = Depends(get_db)):
    service = FinanceService(db)
    entry = service.get_finance_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Finance entry not found")
    return entry


# ===========================================================
# FINANCIAL SUMMARY
# ===========================================================

@router.get("/summary", response_model=FinancialSummary)
def get_financial_summary(
    farm_id: int,
    module_type: str = Query(
        None,
        description="crop | livestock | poultry | aquaculture | hr | store | general",
    ),
    block_id: int | None = None,
    crop_id: int | None = None,
    livestock_id: int | None = None,
    poultry_id: int | None = None,
    aquaculture_id: int | None = None,
    db: Session = Depends(get_db),
):
    service = FinanceService(db)

    module_enum = None
    if module_type:
        try:
            module_enum = ModuleType(module_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid module_type")

    return service.financial_summary(
        farm_id=farm_id,
        module_type=module_enum,
        block_id=block_id,
        crop_id=crop_id,
        livestock_id=livestock_id,
        poultry_id=poultry_id,
        aquaculture_id=aquaculture_id,
    )


# ===========================================================
# INVOICE ENDPOINTS
# ===========================================================

@router.post("/invoices", response_model=InvoiceSchema)
def create_invoice(request: InvoiceCreate, db: Session = Depends(get_db)):
    service = FinanceService(db)
    return service.create_invoice(request.dict())


@router.get("/invoices/{invoice_id}", response_model=InvoiceSchema)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    service = FinanceService(db)
    invoice = service.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


# ===========================================================
# PAYMENT ENDPOINTS
# ===========================================================

@router.post("/payments", response_model=PaymentSchema)
def create_payment(request: PaymentCreate, db: Session = Depends(get_db)):
    service = FinanceService(db)
    return service.create_payment(request.dict())


@router.get("/payments/{payment_id}", response_model=PaymentSchema)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    service = FinanceService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# ===========================================================
# FINANCIAL SUMMARY PDF EXPORT
# ===========================================================

@router.get("/summary/pdf")
def financial_summary_pdf(
    farm_id: int,
    module_type: str = Query(None),
    block_id: int | None = None,
    crop_id: int | None = None,
    livestock_id: int | None = None,
    poultry_id: int | None = None,
    aquaculture_id: int | None = None,
    db: Session = Depends(get_db),
):
    service = FinanceService(db)

    module_enum = None
    if module_type:
        try:
            module_enum = ModuleType(module_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid module_type")

    summary = service.financial_summary(
        farm_id=farm_id,
        module_type=module_enum,
        block_id=block_id,
        crop_id=crop_id,
        livestock_id=livestock_id,
        poultry_id=poultry_id,
        aquaculture_id=aquaculture_id,
    )

    report_service = FinanceReportService(db)
    pdf_file = report_service.generate_financial_summary_pdf(summary.dict())

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=financial_summary_{date.today()}.pdf"
        },
    )


# ===========================================================
# EXPORT FINANCE TABLES (PDF / EXCEL)
# ===========================================================

@router.get("/export/{table_name}")
def export_finance(
    table_name: str,
    format: str = Query("excel", regex="^(excel|pdf)$"),
    farm_id: int | None = None,
    module_type: str = Query(None),
    block_id: int | None = None,
    crop_id: int | None = None,
    livestock_id: int | None = None,
    poultry_id: int | None = None,
    aquaculture_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    report_service = FinanceReportService(db)

    module_enum = None
    if module_type:
        try:
            module_enum = ModuleType(module_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid module_type")

    filters = {
        "farm_id": farm_id,
        "module_type": module_enum,
        "block_id": block_id,
        "crop_id": crop_id,
        "livestock_id": livestock_id,
        "poultry_id": poultry_id,
        "aquaculture_id": aquaculture_id,
        "start_date": start_date,
        "end_date": end_date,
    }

    records, error = report_service.get_records(table_name, **filters)
    if error:
        raise HTTPException(status_code=404, detail=error)

    if format == "excel":
        file = report_service.export_excel(records, table_name)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ext = "xlsx"
    else:
        file = report_service.export_pdf(records, table_name)
        media_type = "application/pdf"
        ext = "pdf"

    return StreamingResponse(
        file,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={table_name}_{date.today()}.{ext}"
        },
    )
