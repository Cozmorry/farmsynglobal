#backend/modules/hr/report_export_router.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from io import BytesIO
from datetime import date
from fastapi.responses import StreamingResponse
import pandas as pd

from backend.core.database import get_db
from backend.modules.hr import models as hr_models
from backend.core.utils.pdf_utils import generate_pdf  # New table-friendly PDF generator

router = APIRouter(tags=["HR Report Exports"])

MODEL_MAP = {
    "permanent_staff": hr_models.PermanentStaff,
    "casual_workers": hr_models.CasualWorker,
    "hr_work_sessions": hr_models.HRWorkSession,
    "hr_payments": hr_models.HRPayment,
    "payroll": hr_models.Payroll
}


def format_record_for_export(record: dict, nested: bool = True):
    """
    Format SQLAlchemy record for export:
    - Convert dates to strings
    - Handle None
    - Include nested relationships (if nested=True)
    """
    formatted = {}
    for key, value in record.items():
        if key.startswith("_"):
            continue
        if value is None:
            formatted[key] = ""
        elif isinstance(value, date):
            formatted[key] = value.strftime("%Y-%m-%d")
        elif isinstance(value, float):
            formatted[key] = float(value)
        elif nested and hasattr(value, "__iter__") and not isinstance(value, str):
            # Nested relationship
            nested_items = []
            for v in value:
                if hasattr(v, "__dict__"):
                    nested_items.append(
                        format_record_for_export(v.__dict__, nested=False)
                    )
                else:
                    nested_items.append(str(v))
            formatted[key] = nested_items
        else:
            formatted[key] = str(value)
    return formatted


@router.get("/export/{table_name}")
def export_hr_report(
    table_name: str,
    format: str = Query("excel", regex="^(excel|pdf)$"),
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False),
    start_date: date | None = None,
    end_date: date | None = None,
    farm_id: int | None = None,
    staff_id: int | None = None
):
    model = MODEL_MAP.get(table_name.lower())
    if not model:
        return {"error": "Invalid table name"}

    query = db.query(model)
    if hasattr(model, "is_active") and not include_inactive:
        query = query.filter_by(is_active=True)

    if farm_id is not None and hasattr(model, "farm_id"):
        query = query.filter_by(farm_id=farm_id)

    if staff_id is not None:
        if hasattr(model, "staff_id"):
            query = query.filter_by(staff_id=staff_id)
        if hasattr(model, "employee_id"):
            query = query.filter_by(employee_id=staff_id)

    if start_date:
        if hasattr(model, "date"):
            query = query.filter(model.date >= start_date)
        if hasattr(model, "period_start"):
            query = query.filter(model.period_start >= start_date)

    if end_date:
        if hasattr(model, "date"):
            query = query.filter(model.date <= end_date)
        if hasattr(model, "period_end"):
            query = query.filter(model.period_end <= end_date)

    records = [format_record_for_export(r.__dict__) for r in query.all()]

    # ---------------------
    # EXCEL EXPORT
    # ---------------------
    if format == "excel":
        df = pd.DataFrame(records if records else [{"info": "No records found"}])

        # Flatten nested columns for Excel
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
                df[col] = df[col].apply(lambda x: " | ".join(str(i) for i in x) if isinstance(x, list) else str(x))

        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            totals = {col: df[col].sum() for col in numeric_cols}
            for col in df.columns:
                if col not in numeric_cols:
                    totals[col] = "TOTAL"
            df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={table_name}.xlsx"}
        )

    # ---------------------
    # PDF EXPORT
    # ---------------------
    pdf_buffer = generate_pdf(records, title=table_name.replace("_", " ").title())
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={table_name}.pdf"}
    )
