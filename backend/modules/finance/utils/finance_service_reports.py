import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date
from backend.models.finance import Income, Expense, Invoice, Payment
from sqlalchemy.orm import Session

class FinanceReportService:
    def __init__(self, db: Session):
        self.db = db

    # ---------------- Excel Reports ----------------
    def generate_income_report_excel(self, farm_id=None):
        query = self.db.query(Income)
        if farm_id:
            query = query.filter(Income.farm_id == farm_id)
        incomes = query.all()

        data = [{
            "ID": i.id,
            "Description": i.description,
            "Amount": i.amount,
            "Source": i.source,
            "Category": i.category,
            "Date": i.date
        } for i in incomes]

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False, engine='xlsxwriter')
        output.seek(0)
        return output

    def generate_expense_report_excel(self, farm_id=None):
        query = self.db.query(Expense)
        if farm_id:
            query = query.filter(Expense.farm_id == farm_id)
        expenses = query.all()

        data = [{
            "ID": e.id,
            "Description": e.description,
            "Amount": e.amount,
            "Category": e.category,
            "Date": e.date,
            "Status": e.status
        } for e in expenses]

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False, engine='xlsxwriter')
        output.seek(0)
        return output

    def generate_invoice_report_excel(self, farm_id=None):
        query = self.db.query(Invoice)
        if farm_id:
            query = query.filter(Invoice.farm_id == farm_id)
        invoices = query.all()

        data = [{
            "ID": inv.id,
            "Invoice Number": inv.invoice_number,
            "Description": inv.description,
            "Amount": inv.amount,
            "Date Issued": inv.date_issued,
            "Due Date": inv.due_date,
            "Status": inv.status
        } for inv in invoices]

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False, engine='xlsxwriter')
        output.seek(0)
        return output

    def generate_payment_report_excel(self, farm_id=None):
        query = self.db.query(Payment)
        if farm_id:
            query = query.filter(Payment.farm_id == farm_id)
        payments = query.all()

        data = [{
            "ID": p.id,
            "Reference": p.payment_reference,
            "Amount": p.amount,
            "Date Paid": p.date_paid,
            "Method": p.method,
            "Invoice ID": p.invoice_id
        } for p in payments]

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False, engine='xlsxwriter')
        output.seek(0)
        return output

    # ---------------- PDF Reports ----------------
    def generate_financial_summary_pdf(self, summary_data: dict):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Financial Summary Report")

        c.setFont("Helvetica", 12)
        y = height - 80
        for key, value in summary_data.items():
            c.drawString(50, y, f"{key}: {value}")
            y -= 20

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

