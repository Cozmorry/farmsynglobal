# backend/core/database.py

import importlib
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# --------------------
# ENGINE & BASE
# --------------------
DATABASE_URL = os.getenv("DATABASE_URL")  # use env variable
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --------------------
# INIT DB
# --------------------
def init_db():
    module_order = [
        "users",
        "farms",
        "audit",
        "store_inventory",
        "crop_management",
        "agronomy",
        "livestock",
        "poultry",
        "veterinary",
        "aquaculture",
        "finance",
        "weather",
        "hr",
        "auth",
    ]

    for module_name in module_order:
        models_path = f"backend.modules.{module_name}.models"
        print(f"Trying to import {models_path}...")
        try:
            importlib.import_module(models_path)
            print(f"[OK] Loaded models for module: {module_name}")
        except ModuleNotFoundError:
            print(f"[SKIP] Module '{module_name}': models.py not found")
        except Exception as e:
            print(f"[FAIL] Failed to load models for '{module_name}': {e}")

    Base.metadata.create_all(bind=engine)
    print("\n[SUCCESS] All database tables created/verified!")

# --------------------
# DATABASE SESSION DEPENDENCY
# --------------------
def get_db():
    """
    Provides a SQLAlchemy session for dependency injection in FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
