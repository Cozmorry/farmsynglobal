# backend/modules/finance/services.py

from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.modules.finance.models import (
    FinanceBase,
    FinanceCrop,
    FinanceLivestock,
    FinancePoultry,
    FinanceAquaculture,
    FinanceHR,
    FinanceInventory,
    ProfitLoss,
    Invoice,
    Payment,
    ModuleType
)

from backend.modules.finance.schemas import FinancialSummary


class FinanceService:
    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------------------------------
    # CREATE FINANCE ENTRY (ATOMIC & SAFE)
    # -----------------------------------------------------------
    def create_finance_entry(self, data: dict):
        """
        Create FinanceBase and its module-specific detail atomically.
        """

        if not data.get("date"):
            data["date"] = date.today()

        module_type = data.get("module_type")

        # -----------------------------
        # VALIDATION PER MODULE
        # -----------------------------
        if module_type == ModuleType.crop:
            if not data.get("crop_id") or not data.get("block_id"):
                raise ValueError("crop_id and block_id are required for crop finance")

        elif module_type == ModuleType.livestock:
            if not data.get("livestock_id"):
                raise ValueError("livestock_id is required for livestock finance")

        elif module_type == ModuleType.poultry:
            if not data.get("poultry_id"):
                raise ValueError("poultry_id is required for poultry finance")

        elif module_type == ModuleType.aquaculture:
            if not data.get("aquaculture_id"):
                raise ValueError("aquaculture_id is required for aquaculture finance")

        elif module_type == ModuleType.hr:
            if not data.get("staff_id"):
                raise ValueError("staff_id is required for HR finance")

        elif module_type == ModuleType.store:
            if not data.get("transaction_id"):
                raise ValueError("transaction_id is required for inventory finance")

        # -----------------------------
        # BASE ENTRY
        # -----------------------------
        finance_entry = FinanceBase(
            description=data["description"],
            amount=data["amount"],
            category=data["category"],
            source=data.get("source", "Manual Entry"),
            date=data["date"],
            receipt_file=data.get("receipt_file"),
            uploaded_by=data.get("uploaded_by"),
            farm_id=data["farm_id"],
            module_type=module_type,
            linked_entity_id=data.get("linked_entity_id"),
        )

        self.db.add(finance_entry)
        self.db.flush()  # get finance_entry.id without committing

        # -----------------------------
        # MODULE-SPECIFIC DETAILS
        # -----------------------------
        if module_type == ModuleType.crop:
            self.db.add(
                FinanceCrop(
                    base_id=finance_entry.id,
                    crop_id=data["crop_id"],
                    block_id=data["block_id"]
                )
            )

        elif module_type == ModuleType.livestock:
            self.db.add(
                FinanceLivestock(
                    base_id=finance_entry.id,
                    livestock_id=data["livestock_id"],
                    reference_id=data.get("linked_entity_id")
                )
            )

        elif module_type == ModuleType.poultry:
            self.db.add(
                FinancePoultry(
                    base_id=finance_entry.id,
                    poultry_id=data["poultry_id"],
                    reference_id=data.get("linked_entity_id")
                )
            )

        elif module_type == ModuleType.aquaculture:
            self.db.add(
                FinanceAquaculture(
                    base_id=finance_entry.id,
                    aquaculture_id=data["aquaculture_id"],
                    reference_id=data.get("linked_entity_id")
                )
            )

        elif module_type == ModuleType.hr:
            self.db.add(
                FinanceHR(
                    base_id=finance_entry.id,
                    staff_id=data["staff_id"],
                    reference_id=data.get("linked_entity_id")
                )
            )

        elif module_type == ModuleType.store:
            self.db.add(
                FinanceInventory(
                    base_id=finance_entry.id,
                    transaction_id=data["transaction_id"]
                )
            )

        # -----------------------------
        # FINAL COMMIT (ATOMIC)
        # -----------------------------
        self.db.commit()
        self.db.refresh(finance_entry)

        return finance_entry

    # -----------------------------------------------------------
    # GET SINGLE ENTRY
    # -----------------------------------------------------------
    def get_finance_entry(self, entry_id: int):
        return (
            self.db.query(FinanceBase)
            .filter(FinanceBase.id == entry_id)
            .first()
        )

    # -----------------------------------------------------------
    # FINANCIAL SUMMARY
    # -----------------------------------------------------------
    def financial_summary(
        self,
        farm_id: int,
        module_type: ModuleType = None,
        crop_id: int = None,
        block_id: int = None,
        livestock_id: int = None,
        poultry_id: int = None,
        aquaculture_id: int = None
    ):
        query = self.db.query(FinanceBase).filter(
            FinanceBase.farm_id == farm_id
        )

        if module_type:
            query = query.filter(FinanceBase.module_type == module_type)

        if module_type == ModuleType.crop:
            query = query.join(FinanceCrop)
            if crop_id:
                query = query.filter(FinanceCrop.crop_id == crop_id)
            if block_id:
                query = query.filter(FinanceCrop.block_id == block_id)

        elif module_type == ModuleType.livestock and livestock_id:
            query = query.join(FinanceLivestock).filter(
                FinanceLivestock.livestock_id == livestock_id
            )

        elif module_type == ModuleType.poultry and poultry_id:
            query = query.join(FinancePoultry).filter(
                FinancePoultry.poultry_id == poultry_id
            )

        elif module_type == ModuleType.aquaculture and aquaculture_id:
            query = query.join(FinanceAquaculture).filter(
                FinanceAquaculture.aquaculture_id == aquaculture_id
            )

        total_income = (
            query.filter(FinanceBase.category == "income")
            .with_entities(func.sum(FinanceBase.amount))
            .scalar()
            or 0.0
        )

        total_expense = (
            query.filter(FinanceBase.category == "expense")
            .with_entities(func.sum(FinanceBase.amount))
            .scalar()
            or 0.0
        )

        return FinancialSummary(
            farm_id=farm_id,
            total_income=total_income,
            total_expense=total_expense,
            profit=total_income - total_expense
        )

    # -----------------------------------------------------------
    # INVOICE
    # -----------------------------------------------------------
    def create_invoice(self, data: dict):
        data.setdefault("date_issued", date.today())
        invoice = Invoice(**data)
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def get_invoice(self, invoice_id: int):
        return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()

    # -----------------------------------------------------------
    # PAYMENT
    # -----------------------------------------------------------
    def create_payment(self, data: dict):
        data.setdefault("date_paid", date.today())
        payment = Payment(**data)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_payment(self, payment_id: int):
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    # -----------------------------------------------------------
    # PROFIT & LOSS SNAPSHOT
    # -----------------------------------------------------------
    def update_profit_loss(self, farm_id: int):
        summary = self.financial_summary(farm_id)

        pl = (
            self.db.query(ProfitLoss)
            .filter(ProfitLoss.farm_id == farm_id)
            .first()
        )

        if not pl:
            pl = ProfitLoss(
                farm_id=farm_id,
                total_income=summary.total_income,
                total_expense=summary.total_expense,
                net_profit=summary.profit
            )
            self.db.add(pl)
        else:
            pl.total_income = summary.total_income
            pl.total_expense = summary.total_expense
            pl.net_profit = summary.profit

        self.db.commit()
        self.db.refresh(pl)
        return pl


# -----------------------------------------------------------
# AUTOMATIC EXPENSE HELPER (USED BY OTHER MODULES)
# -----------------------------------------------------------
def record_expense_auto(
    db: Session,
    amount: float,
    description: str,
    module_type: ModuleType,
    farm_id: int,
    linked_entity_id: int = None
):
    service = FinanceService(db)
    return service.create_finance_entry({
        "description": description,
        "amount": amount,
        "category": "expense",
        "module_type": module_type,
        "farm_id": farm_id,
        "linked_entity_id": linked_entity_id
    })
