# backend/modules/finance/finance_automation.py
from sqlalchemy import event, func
from backend.core.database import SessionLocal
from backend.modules.finance.models import (
    FinanceBase,
    FinanceLivestock,
    FinancePoultry,
    FinanceAquaculture,
    FinanceCrop,
    FinancePayroll,
    FinanceInventory,
    ProfitLoss
)

# Module imports
from backend.modules.livestock.models import LivestockExpense, LivestockActivity, LivestockSale
from backend.modules.poultry.models import PoultryActivity, PoultrySale
from backend.modules.aquaculture.models import AquacultureActivity, AquacultureFeeding, AquacultureHarvest
from backend.modules.crop_management.models import CropActivity, CropSale
from backend.modules.hr.models import HRPayment
from backend.modules.store_inventory.models import InventoryTransaction

# -----------------------------
# Helper to create or update finance entry
# -----------------------------
def create_or_update_finance_entry(db, finance_base=None, description=None, amount=0.0, category=None, source_module=None, entity_id=None, farm_id=None, module_type=None):
    if not finance_base:
        finance_base = FinanceBase(
            description=description,
            amount=amount,
            category=category,
            source_module=source_module,
            module_entity_id=entity_id,
            farm_id=farm_id,
            module_type=module_type
        )
        db.add(finance_base)
        db.flush()
    else:
        finance_base.description = description
        finance_base.amount = amount
        finance_base.category = category
    return finance_base

# -----------------------------
# Helper to update Profit & Loss
# -----------------------------
def update_profit_loss(farm_id):
    db = SessionLocal()
    total_income = db.query(func.coalesce(func.sum(FinanceBase.amount), 0.0))\
        .filter(FinanceBase.farm_id == farm_id, FinanceBase.category == "income").scalar()
    total_expense = db.query(func.coalesce(func.sum(FinanceBase.amount), 0.0))\
        .filter(FinanceBase.farm_id == farm_id, FinanceBase.category == "expense").scalar()
    net_profit = total_income - total_expense

    pl = db.query(ProfitLoss).filter_by(farm_id=farm_id).first()
    if not pl:
        pl = ProfitLoss(farm_id=farm_id, total_income=total_income, total_expense=total_expense, net_profit=net_profit)
        db.add(pl)
    else:
        pl.total_income = total_income
        pl.total_expense = total_expense
        pl.net_profit = net_profit
    db.commit()


# -----------------------------
# FINANCE HANDLER (SAFER VERSION)
# -----------------------------
def finance_handler(target, action, module_type, entity_id_attr="id", amount_attr="amount", description_attr=None, farm_id_attr="farm_id", extra_data={}):
    db = SessionLocal()
    try:
        entity_id = getattr(target, entity_id_attr)
        farm_id = getattr(target, farm_id_attr)
        amount = getattr(target, amount_attr, 0.0)
        if not amount and action == "insert":
            return

        description = getattr(target, description_attr) if description_attr else f"{module_type.capitalize()} Entry: {entity_id}"

        # FIXED: Operator precedence issue
        category = (
            "income"
            if ("Sale" in target.__class__.__name__) or (module_type=="inventory" and getattr(target, "transaction_type", "OUT")=="IN")
            else "expense"
        )

        if action == "insert":
            finance_base = create_or_update_finance_entry(
                db,
                description=description,
                amount=amount,
                category=category,
                source_module=target.__class__.__name__,
                entity_id=entity_id,
                farm_id=farm_id,
                module_type=module_type
            )

            # Module-specific linking
            if module_type == "livestock":
                db.add(FinanceLivestock(base_id=finance_base.id, livestock_id=getattr(target, "livestock_id", None)))
            elif module_type == "crop":
                db.add(FinanceCrop(base_id=finance_base.id, crop_id=getattr(target, "crop_id", None), block_id=extra_data.get("block_id")))
            elif module_type == "inventory":
                db.add(FinanceInventory(base_id=finance_base.id, transaction_id=entity_id))

        elif action == "update":
            finance_base = db.query(FinanceBase).filter_by(module_entity_id=entity_id, module_type=module_type).first()
            if finance_base:
                create_or_update_finance_entry(db, finance_base=finance_base, description=description, amount=amount, category=category)

        elif action == "delete":
            finance_base = db.query(FinanceBase).filter_by(module_entity_id=entity_id, module_type=module_type).first()
            if finance_base:
                db.delete(finance_base)

        db.commit()
        update_profit_loss(farm_id)

    except Exception as e:
        db.rollback()
        print(f"[Finance Handler Error] {e}")
        raise
    finally:
        db.close()



# -----------------------------
# LIVESTOCK LISTENERS
# -----------------------------
for cls in [LivestockExpense, LivestockActivity, LivestockSale]:
    @event.listens_for(cls, "after_insert")
    def insert_listener(mapper, connection, target, cls=cls):
        finance_handler(target, "insert", module_type="livestock", amount_attr="total_cost" if hasattr(target, "total_cost") else "amount",
                        description_attr="name" if hasattr(target, "name") else "sub_category", farm_id_attr="livestock.farm_id")

    @event.listens_for(cls, "after_update")
    def update_listener(mapper, connection, target, cls=cls):
        finance_handler(target, "update", module_type="livestock", amount_attr="total_cost" if hasattr(target, "total_cost") else "amount",
                        description_attr="name" if hasattr(target, "name") else "sub_category", farm_id_attr="livestock.farm_id")

    @event.listens_for(cls, "after_delete")
    def delete_listener(mapper, connection, target, cls=cls):
        finance_handler(target, "delete", module_type="livestock", amount_attr="total_cost" if hasattr(target, "total_cost") else "amount",
                        description_attr="name" if hasattr(target, "name") else "sub_category", farm_id_attr="livestock.farm_id")


# -----------------------------
# POULTRY LISTENERS
# -----------------------------
for cls, module_type in [(PoultryActivity, "poultry"), (PoultrySale, "poultry")]:
    @event.listens_for(cls, "after_insert")
    def insert_listener(mapper, connection, target, cls=cls, module_type=module_type):
        finance_handler(target, "insert", module_type=module_type, amount_attr="total_cost" if hasattr(target, "total_cost") else "total_amount",
                        description_attr="activity_type" if hasattr(target, "activity_type") else "sale_type",
                        farm_id_attr="batch.farm_id")

    @event.listens_for(cls, "after_update")
    def update_listener(mapper, connection, target, cls=cls, module_type=module_type):
        finance_handler(target, "update", module_type=module_type, amount_attr="total_cost" if hasattr(target, "total_cost") else "total_amount",
                        description_attr="activity_type" if hasattr(target, "activity_type") else "sale_type",
                        farm_id_attr="batch.farm_id")

    @event.listens_for(cls, "after_delete")
    def delete_listener(mapper, connection, target, cls=cls, module_type=module_type):
        finance_handler(target, "delete", module_type=module_type, amount_attr="total_cost" if hasattr(target, "total_cost") else "total_amount",
                        description_attr="activity_type" if hasattr(target, "activity_type") else "sale_type",
                        farm_id_attr="batch.farm_id")


# -----------------------------
# AQUACULTURE LISTENERS
# -----------------------------
for cls, module_type, amount_attr, description_attr, farm_id_attr, extra_data_func in [
        (AquacultureActivity, "aquaculture", "cost", "activity_type", "pond.farm_id", None),
        (AquacultureHarvest, "aquaculture", "total_value", None, "pond.farm_id", lambda t: {"pond_id": t.pond_id})
]:
    @event.listens_for(cls, "after_insert")
    def insert_listener(mapper, connection, target, cls=cls, module_type=module_type, amount_attr=amount_attr, description_attr=description_attr, farm_id_attr=farm_id_attr, extra_data_func=extra_data_func):
        extra_data = extra_data_func(target) if extra_data_func else {}
        finance_handler(target, "insert", module_type=module_type, amount_attr=amount_attr, description_attr=description_attr, farm_id_attr=farm_id_attr, extra_data=extra_data)

    @event.listens_for(cls, "after_update")
    def update_listener(mapper, connection, target, cls=cls, module_type=module_type, amount_attr=amount_attr, description_attr=description_attr, farm_id_attr=farm_id_attr, extra_data_func=extra_data_func):
        extra_data = extra_data_func(target) if extra_data_func else {}
        finance_handler(target, "update", module_type=module_type, amount_attr=amount_attr, description_attr=description_attr, farm_id_attr=farm_id_attr, extra_data=extra_data)

    @event.listens_for(cls, "after_delete")
    def delete_listener(mapper, connection, target, cls=cls, module_type=module_type, amount_attr=amount_attr, description_attr=description_attr, farm_id_attr=farm_id_attr, extra_data_func=extra_data_func):
        finance_handler(target, "delete", module_type=module_type, amount_attr=amount_attr, description_attr=description_attr, farm_id_attr=farm_id_attr)


# -----------------------------
# CROP LISTENERS
# -----------------------------
for cls in [CropActivity, CropSale]:
    @event.listens_for(cls, "after_insert")
    def insert_listener(mapper, connection, target, cls=cls):
        extra_data = {"block_id": getattr(target, "block_id", None)}
        finance_handler(target, "insert", module_type="crop", amount_attr="total_cost" if hasattr(target, "total_cost") else "total_amount",
                        description_attr="activity_type" if hasattr(target, "activity_type") else "crop_type",
                        farm_id_attr="farm_id", extra_data=extra_data)

    @event.listens_for(cls, "after_update")
    def update_listener(mapper, connection, target, cls=cls):
        extra_data = {"block_id": getattr(target, "block_id", None)}
        finance_handler(target, "update", module_type="crop", amount_attr="total_cost" if hasattr(target, "total_cost") else "total_amount",
                        description_attr="activity_type" if hasattr(target, "activity_type") else "crop_type",
                        farm_id_attr="farm_id", extra_data=extra_data)

    @event.listens_for(cls, "after_delete")
    def delete_listener(mapper, connection, target, cls=cls):
        finance_handler(target, "delete", module_type="crop", amount_attr="total_cost" if hasattr(target, "total_cost") else "total_amount",
                        description_attr="activity_type" if hasattr(target, "activity_type") else "crop_type",
                        farm_id_attr="farm_id", extra_data={"block_id": getattr(target, "block_id", None)})


# -----------------------------
# HR LISTENERS
# -----------------------------
@event.listens_for(HRPayment, "after_insert")
def hr_payment_insert(mapper, connection, target):
    finance_handler(target, "insert", module_type="hr", amount_attr="amount", description_attr=None, farm_id_attr="farm_id")

@event.listens_for(HRPayment, "after_update")
def hr_payment_update(mapper, connection, target):
    finance_handler(target, "update", module_type="hr", amount_attr="amount", description_attr=None, farm_id_attr="farm_id")

@event.listens_for(HRPayment, "after_delete")
def hr_payment_delete(mapper, connection, target):
    finance_handler(target, "delete", module_type="hr", amount_attr="amount", description_attr=None, farm_id_attr="farm_id")


# -----------------------------
# INVENTORY LISTENERS
# -----------------------------
@event.listens_for(InventoryTransaction, "after_insert")
def inventory_insert(mapper, connection, target):
    finance_handler(target, "insert", module_type="inventory", amount_attr="total_cost", description_attr="description", farm_id_attr="item.farm_id")

@event.listens_for(InventoryTransaction, "after_update")
def inventory_update(mapper, connection, target):
    finance_handler(target, "update", module_type="inventory", amount_attr="total_cost", description_attr="description", farm_id_attr="item.farm_id")

@event.listens_for(InventoryTransaction, "after_delete")
def inventory_delete(mapper, connection, target):
    finance_handler(target, "delete", module_type="inventory", amount_attr="total_cost", description_attr="description", farm_id_attr="item.farm_id")
