from sqlalchemy.orm import Session
from sqlalchemy import and_
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from backend.core.database import Base
from backend.modules.finance.models import FinanceBase


class FinanceReportService:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------------
    # Model Resolver
    # -------------------------------------------------------
    def _get_model(self, name: str):
        """
        Fetch model class from SQLAlchemy registry without direct import.
        Works because all models inherit Base.
        """
        return Base._decl_class_registry.get(name)

    # -------------------------------------------------------
    # GET RECORDS WITH FILTERS
    # -------------------------------------------------------
    def get_records(self, table_name: str, **filters):
        """
        Fetch records from finance tables with date & module filtering.

        Supports:
        - finance (FinanceBase)
        - finance_crop
        - finance_livestock
        - finance_poultry
        - finance_aquaculture
        - finance_hr
        - finance_inventory
        - invoice
        - payment
        """
        model_map = {
            "finance": self._get_model("FinanceBase"),
            "finance_crop": self._get_model("FinanceCrop"),
            "finance_livestock": self._get_model("FinanceLivestock"),
            "finance_poultry": self._get_model("FinancePoultry"),
            "finance_aquaculture": self._get_model("FinanceAquaculture"),
            "finance_hr": self._get_model("FinanceHR"),
            "finance_inventory": self._get_model("FinanceInventory"),
            "invoice": self._get_model("Invoice"),
            "payment": self._get_model("Payment"),
        }

        Model = model_map.get(table_name.lower())
        if not Model:
            return None, f"Table '{table_name}' not found."

        query = self.db.query(Model)

        start_date = filters.get("start_date")
        end_date = filters.get("end_date")

        # =====================================================
        # BASE FINANCE TABLE (finance_base)
        # =====================================================
        if Model.__tablename__ == "finance_base":

            if filters.get("farm_id"):
                query = query.filter(Model.farm_id == filters["farm_id"])

            if filters.get("module_type"):
                query = query.filter(Model.module_type == filters["module_type"])

            if start_date:
                query = query.filter(Model.date >= start_date)

            if end_date:
                query = query.filter(Model.date <= end_date)

        # =====================================================
        # MODULE-SPECIFIC TABLES (crop / livestock / etc.)
        # =====================================================
        elif Model.__tablename__ in [
            "finance_crop",
            "finance_livestock",
            "finance_poultry",
            "finance_aquaculture",
            "finance_hr",
            "finance_inventory"
        ]:

            # ALWAYS JOIN FINANCE_BASE
            query = query.join(Model.base)

            if filters.get("farm_id"):
                query = query.filter(FinanceBase.farm_id == filters["farm_id"])

            # module-specific filtering
            module_filters = [
                "crop_id", "block_id",
                "livestock_id", "poultry_id",
                "aquaculture_id", "staff_id",
                "transaction_id"
            ]

            for key in module_filters:
                if filters.get(key) is not None and hasattr(Model, key):
                    query = query.filter(getattr(Model, key) == filters[key])

            # Date range via FinanceBase
            if start_date:
                query = query.filter(FinanceBase.date >= start_date)
            if end_date:
                query = query.filter(FinanceBase.date <= end_date)

        # =====================================================
        # INVOICE + PAYMENT TABLES
        # =====================================================
        elif Model.__tablename__ in ["invoices", "payments"]:

            # detect correct date column
            date_field = (
                getattr(Model, "date", None)
                or getattr(Model, "date_issued", None)
                or getattr(Model, "date_paid", None)
            )

            if date_field:
                if start_date:
                    query = query.filter(date_field >= start_date)
                if end_date:
                    query = query.filter(date_field <= end_date)

            if filters.get("farm_id") and hasattr(Model, "farm_id"):
                query = query.filter(Model.farm_id == filters["farm_id"])

        # =====================================================
        # Pagination & column selection
        # =====================================================
        skip = filters.get("skip", 0)
        limit = filters.get("limit", 1000)
        query = query.offset(skip).limit(limit)

        columns = filters.get("columns")
        if columns:
            query = query.with_entities(
                *[getattr(Model, c) for c in columns if hasattr(Model, c)]
            )

        return query.all(), None

    # -------------------------------------------------------
    # EXPORT EXCEL
    # -------------------------------------------------------
    def export_excel(self, records, table_name: str):
        df = pd.DataFrame([r.__dict__ for r in records])
        df = df.drop(columns=["_sa_instance_state"], errors="ignore")

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name=table_name.capitalize(), index=False)

        output.seek(0)
        return output

    # -------------------------------------------------------
    # EXPORT PDF
    # -------------------------------------------------------
    def export_pdf(self, records, table_name: str):
        output = BytesIO()
        c = canvas.Canvas(output)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 800, f"{table_name.capitalize()} Report")

        y = 760
        c.setFont("Helvetica", 10)

        if not records:
            c.drawString(50, y, "No records found.")
        else:
            for r in records:
                row = ", ".join(
                    f"{k}: {v}"
                    for k, v in r.__dict__.items()
                    if k != "_sa_instance_state"
                )

                if y < 40:
                    c.showPage()
                    y = 800
                c.drawString(50, y, row)
                y -= 18

        c.showPage()
        c.save()
        output.seek(0)
        return output

    # -------------------------------------------------------
    # FINANCIAL SUMMARY PDF
    # -------------------------------------------------------
    def generate_financial_summary_pdf(self, summary: dict):
        output = BytesIO()
        c = canvas.Canvas(output)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, "Financial Summary Report")

        c.setFont("Helvetica", 12)
        y = 760

        for key, value in summary.items():
            if y < 40:
                c.showPage()
                y = 800
            c.drawString(50, y, f"{key}: {value}")
            y -= 20

        c.showPage()
        c.save()
        output.seek(0)
        return output
