#backend/modules/store_inventory/services.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from .models import (
    StoreItem,
    InventoryTransaction,
    TransactionType,
    ModuleType,
)
from .schemas import (
    StoreItemCreate,
    StoreItemUpdate,
    InventoryTransactionCreate,
    InventoryTransactionUpdate
)
from backend.core.utils.product_enrichment import get_product_details


# ============================================================================
# STORE ITEM SERVICES
# ============================================================================

def create_store_item(db: Session, data: StoreItemCreate):
    """
    Create a store item with product enrichment.
    """

    metadata = get_product_details(data.name)

    enriched_fields = {
        "manufacturer": metadata.get("manufacturer"),
        "active_ingredients": metadata.get("active_ingredient"),
        "composition": metadata.get("composition"),
        "product_website": metadata.get("product_website"),
        "safety_precautions": metadata.get("safety_precautions")
    }

    item = StoreItem(
        **data.model_dump(),
        **{k: v for k, v in enriched_fields.items() if v}
    )

    item.total_value = item.quantity_in_stock * item.unit_cost

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_store_item(db: Session, item_id: int, data: StoreItemUpdate):
    """
    Update item fields and recompute total value.
    """

    item = (
        db.query(StoreItem)
        .filter(StoreItem.id == item_id, StoreItem.is_deleted == False)
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    item.total_value = item.quantity_in_stock * item.unit_cost

    db.commit()
    db.refresh(item)
    return item


def soft_delete_store_item(db: Session, item_id: int):
    item = db.query(StoreItem).filter(StoreItem.id == item_id).first()

    if not item or item.is_deleted:
        raise HTTPException(status_code=404, detail="Item already deleted")

    item.is_deleted = True
    item.deleted_at = datetime.utcnow()

    db.commit()
    return {"message": "Item deleted"}


def restore_store_item(db: Session, item_id: int):
    item = db.query(StoreItem).filter(StoreItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.is_deleted = False
    item.deleted_at = None

    db.commit()
    return {"message": "Item restored"}


# ============================================================================
# TRANSACTION SERVICES
# ============================================================================

def record_transaction(db: Session, data: InventoryTransactionCreate):
    """
    Record stock transaction, adjust stock, compute value, and optionally link to modules.
    """

    item = db.query(StoreItem).filter(StoreItem.id == data.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Store item not found")

    purchase_qty = data.quantity * item.conversion_factor

    # -----------------------------
    # VALIDATION FOR OUT
    # -----------------------------
    if data.transaction_type == TransactionType.OUT:
        if item.quantity_in_stock < purchase_qty:
            raise HTTPException(status_code=400, detail="Insufficient stock")

    # -----------------------------
    # APPLY STOCK IMPACT
    # -----------------------------
    if data.transaction_type == TransactionType.IN:
        item.quantity_in_stock += purchase_qty

    elif data.transaction_type == TransactionType.OUT:
        item.quantity_in_stock -= purchase_qty
        item.quantity_used += purchase_qty

    elif data.transaction_type == TransactionType.ADJUSTMENT:
        item.quantity_in_stock = purchase_qty

    # -----------------------------
    # COST
    # -----------------------------
    total_cost = (data.unit_cost or item.unit_cost) * purchase_qty

    trans = InventoryTransaction(
        **data.model_dump(),
        quantity=data.quantity,
        total_cost=total_cost,
        unit_cost=data.unit_cost or item.unit_cost,
        date=data.date or datetime.utcnow(),
    )

    # Recompute value
    item.total_value = item.quantity_in_stock * item.unit_cost

    db.add(trans)
    db.commit()
    db.refresh(trans)
    return trans


def update_transaction(db: Session, transaction_id: int, data: InventoryTransactionUpdate):
    trans = (
        db.query(InventoryTransaction)
        .filter(InventoryTransaction.id == transaction_id, InventoryTransaction.is_deleted == False)
        .first()
    )

    if not trans:
        raise HTTPException(status_code=404, detail="Transaction not found")

    item = trans.item

    # Reverse previous impact
    _reverse_stock_effect(item, trans)

    # Apply updates
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(trans, field, value)

    # Apply new effect
    _apply_stock_effect(item, trans)

    db.commit()
    db.refresh(trans)
    return trans


def soft_delete_transaction(db: Session, transaction_id: int):
    trans = db.query(InventoryTransaction).filter(InventoryTransaction.id == transaction_id).first()

    if not trans or trans.is_deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")

    item = trans.item

    _reverse_stock_effect(item, trans)

    trans.is_deleted = True
    trans.deleted_at = datetime.utcnow()

    db.commit()
    return {"message": "Transaction deleted"}


# ============================================================================
# INTERNAL HELPERS
# ============================================================================

def _reverse_stock_effect(item: StoreItem, trans: InventoryTransaction):
    qty = trans.quantity * item.conversion_factor

    if trans.transaction_type == TransactionType.IN:
        item.quantity_in_stock -= qty

    elif trans.transaction_type == TransactionType.OUT:
        item.quantity_in_stock += qty
        item.quantity_used -= qty

    elif trans.transaction_type == TransactionType.ADJUSTMENT:
        # no reliable reverse for adjustment
        pass

    item.total_value = item.quantity_in_stock * item.unit_cost


def _apply_stock_effect(item: StoreItem, trans: InventoryTransaction):
    qty = trans.quantity * item.conversion_factor

    if trans.transaction_type == TransactionType.IN:
        item.quantity_in_stock += qty

    elif trans.transaction_type == TransactionType.OUT:
        item.quantity_in_stock -= qty
        item.quantity_used += qty

    elif trans.transaction_type == TransactionType.ADJUSTMENT:
        item.quantity_in_stock = qty

    item.total_value = item.quantity_in_stock * item.unit_cost

