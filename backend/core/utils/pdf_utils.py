from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date, datetime


# ============================================================
# ✔ MAIN MULTI-TABLE PDF GENERATOR
# ============================================================
def generate_pdf_multiple_tables(sections, title="Report"):
    """
    Generate a PDF with multiple tables:
    - sections: list of {"title": str, "records": list of dicts}
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=18,
    )
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"<b>{title}</b>", styles['Title']))
    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles['Normal']
        )
    )
    elements.append(Spacer(1, 12))

    for section in sections:
        section_title = section.get("title", "Section")
        records = section.get("records", [])

        elements.append(Paragraph(f"<b>{section_title}</b>", styles['Heading2']))
        elements.append(Spacer(1, 6))

        if not records:
            elements.append(Paragraph("No records found.", styles['Normal']))
            elements.append(Spacer(1, 12))
            continue

        headers = list(records[0].keys())
        data = [headers]

        # Build rows
        for rec in records:
            row = []
            for h in headers:
                value = rec[h]
                if isinstance(value, (date, datetime)):
                    value = value.strftime("%Y-%m-%d")
                elif isinstance(value, float):
                    value = f"{value:,.2f}"
                row.append(str(value) if value is not None else "")
            data.append(row)

        # Auto column width
        col_widths = []
        for col_idx in range(len(headers)):
            max_len = max(len(str(row[col_idx])) for row in data)
            width = min(max_len * 6, 200)
            col_widths.append(width)

        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#DCE6F1")]),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# ============================================================
# ✔ WRAPPER FOR BACKWARD COMPATIBILITY
# This fixes the "cannot import name generate_pdf" error
# ============================================================
def generate_pdf(data, title="Report"):
    """
    Backwards-compatible wrapper.
    Accepts a single list of dicts and creates a single-table PDF.
    """
    sections = [{"title": title, "records": data}]
    return generate_pdf_multiple_tables(sections, title)
