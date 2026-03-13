# tests/test_livestock_full.py
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.database import Base
from backend.modules.livestock import models, services, schemas

# -----------------------------
# Setup in-memory DB for testing
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

# -----------------------------
# Mock external dependencies
# -----------------------------
def mock_reduce_inventory_stock(db, item_name, quantity, cost):
    return True

def mock_record_expense(db, category, amount, description):
    return True

def mock_record_sale(db, category, amount, description):
    return True

services.reduce_inventory_stock = mock_reduce_inventory_stock
services.record_expense = mock_record_expense
services.record_sale = mock_record_sale

# -----------------------------
# LIVESTOCK CRUD
# -----------------------------
def test_create_livestock(db):
    data = schemas.LivestockCreate(
        name="Bessie",
        type="Cattle",
        gender="Female",
        farm_id=1,
        purchase_price=500.0
    )
    livestock = services.create_livestock(db, data)
    assert livestock.id is not None
    assert livestock.name == "Bessie"

def test_get_all_livestock(db):
    all_livestock = services.get_all_livestock(db)
    assert len(all_livestock) > 0

def test_update_livestock(db):
    livestock = services.get_all_livestock(db)[0]
    update_data = schemas.LivestockUpdate(name="Bessie Updated")
    updated = services.update_livestock(db, livestock.id, update_data)
    assert updated.name == "Bessie Updated"

def test_delete_livestock(db):
    livestock = services.get_all_livestock(db)[0]
    response = services.delete_livestock(db, livestock.id)
    assert response["detail"] == "Livestock deleted successfully"

# -----------------------------
# LIVESTOCK GROUPS
# -----------------------------
def test_create_group(db):
    group_data = schemas.LivestockGroupCreate(name="Herd A", farm_id=1)
    group = services.create_group(db, group_data)
    assert group.id is not None
    assert group.name == "Herd A"

def test_assign_to_group(db):
    livestock = services.create_livestock(db, schemas.LivestockCreate(
        name="Moo", type="Cattle", gender="Male", farm_id=1
    ))
    group = services.create_group(db, schemas.LivestockGroupCreate(name="Herd B", farm_id=1))
    assigned = services.assign_to_group(db, livestock.id, group.id)
    assert assigned.group_id == group.id

# -----------------------------
# WEIGHT RECORDS
# -----------------------------
def test_create_weight(db):
    livestock = services.create_livestock(db, schemas.LivestockCreate(
        name="WeightTest", type="Sheep", gender="Female", farm_id=1
    ))
    weight_data = schemas.LivestockWeightRecordCreate(livestock_id=livestock.id, weight=50.0)
    weight = services.create_weight(db, weight_data)
    assert weight.weight == 50.0

# -----------------------------
# PRODUCTION
# -----------------------------
def test_create_production(db):
    livestock = services.create_livestock(db, schemas.LivestockCreate(
        name="Producer", type="Goat", gender="Female", farm_id=1
    ))
    prod_data = schemas.LivestockProductionCreate(
        livestock_id=livestock.id,
        production_type="Milk",
        quantity=10,
        unit_price=5.0
    )
    production = services.create_production(db, prod_data)
    assert production.total_value == 50.0

# -----------------------------
# FEEDING
# -----------------------------
def test_create_feeding(db):
    livestock = services.create_livestock(db, schemas.LivestockCreate(
        name="Feeder", type="Pig", gender="Male", farm_id=1
    ))
    feed_data = schemas.LivestockFeedingCreate(
        livestock_id=livestock.id,
        feed_item_id=1,
        quantity=5,
        feed_type="Corn",
        unit_cost=2.0
    )
    feeding = services.create_feeding(db, feed_data)
    assert feeding.livestock_id == livestock.id
    assert feeding.quantity == 5

# -----------------------------
# ACTIVITIES
# -----------------------------
def test_create_activity(db):
    livestock = services.create_livestock(db, schemas.LivestockCreate(
        name="ActivityTest", type="Cattle", gender="Male", farm_id=1
    ))
    activity_data = schemas.LivestockActivityCreate(
        livestock_id=livestock.id,
        name="Vaccination",
        activity_type="service",
        cost=30.0
    )
    activity = services.create_activity(db, activity_data)
    assert activity.cost == 30.0

# -----------------------------
# EXPENSES
# -----------------------------
def test_create_expense(db):
    livestock = services.create_livestock(db, schemas.LivestockCreate(
        name="ExpenseTest", type="Sheep", gender="Female", farm_id=1
    ))
    expense_data = schemas.LivestockExpenseCreate(
        livestock_id=livestock.id,
        amount=100.0
    )
    expense = services.create_expense(db, expense_data)
    assert expense.amount == 100.0

# -----------------------------
# SALES
# -----------------------------
def test_create_sale(db):
    livestock = services.create_livestock(db, schemas.LivestockCreate(
        name="Seller", type="Goat", gender="Female", farm_id=1
    ))
    sale_data = schemas.LivestockSaleCreate(
        livestock_id=livestock.id,
        production_type="Milk",
        quantity=5,
        unit_price=10
    )
    sale = services.create_sale(db, sale_data)
    assert sale.total_sale == 50
