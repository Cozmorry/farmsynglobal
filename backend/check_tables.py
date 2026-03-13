"""
check_tables.py
Professional ERP table & column checker with summary dashboard
"""

import sqlite3
import sys
from pathlib import Path

# For colored output in terminal
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ""
        RED = ""
        YELLOW = ""
        CYAN = ""
    class Style:
        BRIGHT = ""
        RESET_ALL = ""

# Path to SQLite database
DB_PATH = Path(__file__).parent / "farm.db"

# ERP schema: tables with example columns (adjust as needed)
ERP_SCHEMA = {
    "users": ["id", "username", "email", "password", "role", "created_at", "updated_at"],
    "farms": ["id", "name", "location", "owner_id", "created_at", "updated_at"],
    "crops": ["id", "name", "farm_id", "created_at", "updated_at"],
    "livestock": ["id", "type", "farm_id", "created_at", "updated_at"],
    "aquaculture": ["id", "pond_id", "species", "created_at", "updated_at"],
    "expenses": ["id", "amount", "description", "farm_id", "created_at", "updated_at"],
    "ponds": ["id", "name", "farm_id", "capacity", "created_at", "updated_at"],
    "crop_activities": ["id", "crop_id", "activity_type", "date", "created_at", "updated_at"],
    "alembic_version": ["version_num"],
    "crop_rotation": ["id", "crop_id", "rotation_period", "created_at", "updated_at"],
    "season_end": ["id", "farm_id", "season_date", "created_at", "updated_at"],
    "soil_amendments": ["id", "farm_id", "type", "quantity", "date", "created_at", "updated_at"],
    "soil_tests": ["id", "farm_id", "test_type", "result", "date", "created_at", "updated_at"],
    "store_items": ["id", "name", "quantity", "price", "created_at", "updated_at"],
    "chemical_applications": ["id", "crop_id", "chemical", "quantity", "date", "created_at", "updated_at"],
    "crop_budgets": ["id", "crop_id", "budget", "created_at", "updated_at"],
    "crop_harvests": ["id", "crop_id", "harvest_date", "quantity", "created_at", "updated_at"],
    "crop_sales": ["id", "crop_id", "sale_date", "quantity", "amount", "created_at", "updated_at"],
    "fertilizer_applications": ["id", "crop_id", "fertilizer", "quantity", "date", "created_at", "updated_at"],
    "inventory_transactions": ["id", "item_id", "quantity", "transaction_type", "date", "created_at", "updated_at"],
    "irrigation": ["id", "crop_id", "method", "date", "duration", "created_at", "updated_at"],
    "land_preparation": ["id", "crop_id", "task", "date", "created_at", "updated_at"],
    "nursery_activities": ["id", "activity_type", "crop_id", "date", "created_at", "updated_at"],
    "scouting": ["id", "crop_id", "issue_found", "date", "created_at", "updated_at"],
    "weeding": ["id", "crop_id", "date", "method", "created_at", "updated_at"],
    "animal_groups": ["id", "name", "farm_id", "created_at", "updated_at"],
    "barns": ["id", "name", "capacity", "farm_id", "created_at", "updated_at"],
    "blocks": ["id", "name", "farm_id", "created_at", "updated_at"],
    "casual_workers": ["id", "name", "role", "hours_worked", "payment", "created_at", "updated_at"],
    "coops": ["id", "name", "farm_id", "capacity", "created_at", "updated_at"],
    "hr_payments": ["id", "employee_id", "amount", "date", "created_at", "updated_at"],
    "incomes": ["id", "source", "amount", "date", "created_at", "updated_at"],
    "permanent_staff": ["id", "name", "role", "salary", "created_at", "updated_at"],
    "poultry_batches": ["id", "batch_name", "coop_id", "created_at", "updated_at"],
    "profit_loss": ["id", "farm_id", "period", "profit", "loss", "created_at", "updated_at"],
    "animal_health_records": ["id", "animal_id", "disease", "treatment", "date", "created_at", "updated_at"],
    "aquaculture_activity": ["id", "pond_id", "activity_type", "date", "created_at", "updated_at"],
    "aquaculture_feeding": ["id", "pond_id", "feed_type", "quantity", "date", "created_at", "updated_at"],
    "aquaculture_harvest": ["id", "pond_id", "harvest_date", "quantity", "created_at", "updated_at"],
    "aquaculture_production": ["id", "pond_id", "production_date", "quantity", "created_at", "updated_at"],
    "aquaculture_summary": ["id", "pond_id", "summary_date", "details", "created_at", "updated_at"],
    "aquaculture_water_quality": ["id", "pond_id", "parameter", "value", "date", "created_at", "updated_at"],
    "crop_blocks": ["id", "block_name", "crop_id", "farm_id", "created_at", "updated_at"],
    "greenhouses": ["id", "name", "farm_id", "capacity", "created_at", "updated_at"],
    "livestock_activities": ["id", "animal_id", "activity_type", "date", "created_at", "updated_at"],
    "livestock_expenses": ["id", "animal_id", "expense_type", "amount", "date", "created_at", "updated_at"],
    "livestock_productions": ["id", "animal_id", "product_type", "quantity", "date", "created_at", "updated_at"],
    "livestock_sales": ["id", "animal_id", "sale_date", "quantity", "amount", "created_at", "updated_at"],
    "payroll": ["id", "employee_id", "salary", "date", "created_at", "updated_at"],
    "poultry_activities": ["id", "poultry_batch_id", "activity_type", "date", "created_at", "updated_at"],
    "poultry_production": ["id", "poultry_batch_id", "product_type", "quantity", "date", "created_at", "updated_at"],
    "poultry_sales": ["id", "poultry_batch_id", "sale_date", "quantity", "amount", "created_at", "updated_at"],
    "weather_data": ["id", "farm_id", "date", "temperature", "humidity", "rainfall", "created_at", "updated_at"],
    "weather_observations": ["id", "farm_id", "date", "observation", "created_at", "updated_at"],
    "agronomy_recommendations": ["id", "crop_id", "recommendation", "date", "created_at", "updated_at"],
    "hr_work_sessions": ["id", "employee_id", "task", "date", "hours", "created_at", "updated_at"],
    "veterinary_recommendations": ["id", "animal_id", "recommendation", "date", "created_at", "updated_at"],
}

def connect_db(db_path: Path):
    if not db_path.exists():
        print(f"{Fore.RED}❌ Database file not found at {db_path}")
        sys.exit(1)
    return sqlite3.connect(db_path)

def get_existing_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {}
    for row in cursor.fetchall():
        table_name = row[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        tables[table_name] = columns
    return tables

def summarize(existing_tables):
    total_tables_expected = len(ERP_SCHEMA)
    total_tables_found = len(existing_tables)
    missing_tables = [t for t in ERP_SCHEMA if t not in existing_tables]
    total_missing_tables = len(missing_tables)

    total_columns_expected = sum(len(cols) for cols in ERP_SCHEMA.values())
    total_columns_found = sum(len(cols) for table, cols in existing_tables.items() if table in ERP_SCHEMA)
    missing_columns_overall = {}
    for table, expected_cols in ERP_SCHEMA.items():
        if table in existing_tables:
            missing_cols = [col for col in expected_cols if col not in existing_tables[table]]
            if missing_cols:
                missing_columns_overall[table] = missing_cols

    return {
        "total_tables_expected": total_tables_expected,
        "total_tables_found": total_tables_found,
        "total_missing_tables": total_missing_tables,
        "missing_tables": missing_tables,
        "total_columns_expected": total_columns_expected,
        "total_columns_found": total_columns_found,
        "missing_columns_overall": missing_columns_overall
    }

def display_dashboard(existing_tables):
    print(f"{Fore.CYAN}{Style.BRIGHT}📘 ERP Database Summary Dashboard\n")
    summary = summarize(existing_tables)

    print(f"{Fore.GREEN}{Style.BRIGHT}✅ Tables Found: {summary['total_tables_found']} / {summary['total_tables_expected']}")
    if summary['missing_tables']:
        print(f"{Fore.RED}⚠️ Missing Tables ({summary['total_missing_tables']}): {', '.join(summary['missing_tables'])}")
    
    print(f"{Fore.GREEN}{Style.BRIGHT}✅ Columns Found: {summary['total_columns_found']} / {summary['total_columns_expected']}")
    if summary['missing_columns_overall']:
        print(f"{Fore.YELLOW}⚠️ Tables with Missing Columns:")
        for table, cols in summary['missing_columns_overall'].items():
            print(f"   - {table}: {cols}")

    if not summary['missing_tables'] and not summary['missing_columns_overall']:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🌾 All ERP tables and columns exist — database is ready for migration ✅")
    else:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}💡 Next step: generate migrations using `alembic revision --autogenerate -m 'Fix missing tables/columns'`")

def main():
    conn = connect_db(DB_PATH)
    existing_tables = get_existing_tables(conn)
    
    if not existing_tables:
        print(f"{Fore.RED}⚠️ No tables found in the database. Migration needed!")
        sys.exit(1)

    display_dashboard(existing_tables)
    conn.close()

if __name__ == "__main__":
    main()
