from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
import pandas as pd
from datetime import datetime, date

from backend.core.database import get_db
from backend.modules.store_inventory.models import StoreItem, InventoryTransaction, ModuleType, ItemCategory
from backend.core.utils.pdf_utils import generate_pdf_multiple_tables

router = APIRouter(
    prefix="/store-inventory/export",
    tags=["Store & Inventory Reports"],
)

# ============================================================================
# EXPORT STORE ITEMS + TRANSACTIONS (WITH FILTERS)
# ============================================================================
@router.get("/full-report")
def export_full_report(
    format: str = Query("excel", enum=["excel", "pdf"]),
    module_type: ModuleType | None = Query(None, description="Filter by module"),
    category: ItemCategory | None = Query(None, description="Filter by item category"),
    start_date: date | None = Query(None, description="Start date for transactions"),
    end_date: date | None = Query(None, description="End date for transactions"),
    db: Session = Depends(get_db)
):
    # ---------------------------
    # FETCH STORE ITEMS
    # ---------------------------
    items_query = db.query(StoreItem).filter(StoreItem.is_deleted == False)
    if module_type:
        items_query = items_query.filter(StoreItem.module_type == module_type)
    if category:
        items_query = items_query.filter(StoreItem.category == category)
    items = items_query.all()

    # ---------------------------
    # FETCH TRANSACTIONS
    # ---------------------------
    tx_query = db.query(InventoryTransaction).filter(InventoryTransaction.is_deleted == False)
    if module_type:
        tx_query = tx_query.filter(InventoryTransaction.module_type == module_type)
    if start_date:
        tx_query = tx_query.filter(InventoryTransaction.date >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        tx_query = tx_query.filter(InventoryTransaction.date <= datetime.combine(end_date, datetime.max.time()))
    transactions = tx_query.all()

    if not items and not transactions:
        raise HTTPException(status_code=404, detail="No data found for the given filters")

    # ---------------------------
    # PREPARE DATA
    # ---------------------------
    items_data = [
        {
            "ID": item.id,
            "Name": item.name,
            "Category": item.category.value,
            "Module": item.module_type.value,
            "Stock": item.quantity_in_stock,
            "Used": item.quantity_used,
            "Unit Cost": item.unit_cost,
            "Total Value": item.total_value,
            "Manufacturer": item.manufacturer,
            "Created At": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for item in items
    ]

    transactions_data = [
        {
            "ID": tx.id,
            "Item Name": tx.item.name if tx.item else None,
            "Transaction Type": tx.transaction_type.value,
            "Quantity": tx.quantity,
            "Unit Cost": tx.unit_cost,
            "Total Cost": tx.total_cost,
            "Module": tx.module_type.value if tx.module_type else None,
            "Date": tx.date.strftime("%Y-%m-%d %H:%M:%S"),
            "Reference": tx.reference,
            "Description": tx.description,
        }
        for tx in transactions
    ]

    # ---------------------------
    # EXPORT TO EXCEL
    # ---------------------------
    if format == "excel":
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            if items_data:
                pd.DataFrame(items_data).to_excel(writer, index=False, sheet_name="Store Items")
            if transactions_data:
                pd.DataFrame(transactions_data).to_excel(writer, index=False, sheet_name="Transactions")
        buffer.seek(0)
        filename = f"store_inventory_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    # ---------------------------
    # EXPORT TO PDF
    # ---------------------------
    elif format == "pdf":
        combined_records = []
        if items_data:
            combined_records.append({"title": "Store Items", "records": items_data})
        if transactions_data:
            combined_records.append({"title": "Inventory Transactions", "records": transactions_data})

        buffer = generate_pdf_multiple_tables(combined_records)
        filename = f"store_inventory_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid format. Choose 'excel' or 'pdf'.")


# ========================================================================
# PDF UTILITY (MULTIPLE TABLES)
# ========================================================================
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_multiple_tables(sections: list[dict]) -> BytesIO:
    """
    sections: List of dicts with keys 'title' and 'records' (list of dicts)
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []
    styles = getSampleStyleSheet()

    for section in sections:
        elements.append(Paragraph(f"<b>{section['title']}</b>", styles['Title']))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Paragraph(" ", styles['Normal']))

        records = section["records"]
        headers = list(records[0].keys())
        data = [headers] + [[str(r[h]) if r[h] is not None else "" for h in headers] for r in records]

        # Column widths
        col_widths = [min(max(len(str(row[i])) for row in data) * 6, 200) for i in range(len(headers))]

        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ]))
        elements.append(table)
        elements.append(Paragraph(" ", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer
