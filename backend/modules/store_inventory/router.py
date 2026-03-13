#backend/modules/store_inventory/router.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from backend.core.database import get_db

from .schemas import (
    StoreItemCreate,
    StoreItemUpdate,
    StoreItemSchema,
    InventoryTransactionCreate,
    InventoryTransactionUpdate,
    InventoryTransactionSchema,
)

from .services import (
    create_store_item,
    update_store_item,
    soft_delete_store_item,
    restore_store_item,
    record_transaction,
    update_transaction,
    soft_delete_transaction,
)


router = APIRouter(tags=["Store & Inventory"])
    


# ============================================================================
# STORE ITEM ROUTES
# ============================================================================

@router.post("/items", response_model=StoreItemSchema)
def create_item(request: StoreItemCreate, db: Session = Depends(get_db)):
    return create_store_item(db, request)


@router.patch("/items/{item_id}", response_model=StoreItemSchema)
def update_item(item_id: int, request: StoreItemUpdate, db: Session = Depends(get_db)):
    return update_store_item(db, item_id, request)


@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return soft_delete_store_item(db, item_id)


@router.put("/items/{item_id}/restore")
def restore_item(item_id: int, db: Session = Depends(get_db)):
    return restore_store_item(db, item_id)


# List items (active only)
@router.get("/items", response_model=List[StoreItemSchema])
def list_items(db: Session = Depends(get_db)):
    from .models import StoreItem
    return (
        db.query(StoreItem)
        .filter(StoreItem.is_deleted == False)
        .order_by(StoreItem.created_at.desc())
        .all()
    )


# ============================================================================
# TRANSACTION ROUTES
# ============================================================================

@router.post("/transactions", response_model=InventoryTransactionSchema)
def create_inventory_transaction(
    request: InventoryTransactionCreate,
    db: Session = Depends(get_db)
):
    return record_transaction(db, request)


@router.patch("/transactions/{trans_id}", response_model=InventoryTransactionSchema)
def update_inventory_transaction(
    trans_id: int,
    request: InventoryTransactionUpdate,
    db: Session = Depends(get_db)
):
    return update_transaction(db, trans_id, request)


@router.delete("/transactions/{trans_id}")
def delete_inventory_transaction(trans_id: int, db: Session = Depends(get_db)):
    return soft_delete_transaction(db, trans_id)


# List transactions
@router.get("/transactions", response_model=List[InventoryTransactionSchema])
def list_transactions(db: Session = Depends(get_db)):
    from .models import InventoryTransaction
    return (
        db.query(InventoryTransaction)
        .filter(InventoryTransaction.is_deleted == False)
        .order_by(InventoryTransaction.date.desc())
        .all()
    )


# -------------------- PDF EXPORT ROUTE --------------------

@router.get("/export/pdf")
def export_store_inventory_pdf(db: Session = Depends(get_db)):
    items = db.query(StoreItem).filter(StoreItem.is_deleted == False).all()
    transactions = db.query(InventoryTransaction).filter(InventoryTransaction.is_deleted == False).all()

    items_data = [{
        "ID": i.id,
        "Name": i.name,
        "Category": i.category.value,
        "Module": i.module_type.value,
        "Stock": i.quantity_in_stock,
        "Used": i.quantity_used,
        "Unit Cost": i.unit_cost,
        "Total Value": i.total_value
    } for i in items]

    transactions_data = [{
        "ID": t.id,
        "Item": t.item.name if t.item else "",
        "Type": t.transaction_type.value,
        "Quantity": t.quantity,
        "Unit Cost": t.unit_cost,
        "Total Cost": t.total_cost,
        "Date": t.date.strftime("%Y-%m-%d %H:%M:%S"),
        "Recorded By": t.recorded_by
    } for t in transactions]

    sections = [
        {"title": "Store Items", "records": items_data},
        {"title": "Transactions", "records": transactions_data}
    ]

    pdf_buffer = generate_pdf_multiple_tables(sections, title="Store Inventory Report")

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=store_inventory_report.pdf"}
    )


