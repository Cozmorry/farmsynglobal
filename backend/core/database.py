# backend/core/database.py

import importlib
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import make_url
import os
from dotenv import load_dotenv

load_dotenv()

# --------------------
# ENSURE MYSQL DATABASE EXISTS
# --------------------
def _ensure_mysql_db(url_str: str) -> None:
    """Create MySQL database if it doesn't exist."""
    try:
        url = make_url(url_str)
        if url.drivername and "mysql" in url.drivername and url.database:
            import pymysql
            conn = pymysql.connect(
                host=url.host or "localhost",
                port=url.port or 3306,
                user=url.username,
                password=url.password or "",
                charset="utf8mb4",
            )
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{url.database}`")
            conn.commit()
            conn.close()
    except Exception as e:
        import logging
        logging.warning(f"Could not auto-create MySQL database: {e}")

# --------------------
# ENGINE & BASE
# --------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    _ensure_mysql_db(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --------------------
# INIT DB
# --------------------
def init_db():
    module_order = [
        "users",
        "tenants",
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

    try:
        Base.metadata.create_all(bind=engine)
        print("\n[SUCCESS] All database tables created/verified!")
    except OperationalError as e:
        # MySQL 1050 = table already exists (from previous/partial run)
        err_code = getattr(getattr(e, "orig", None), "args", [None])[0]
        if err_code == 1050:
            print("\n[INFO] Tables already exist; schema up-to-date.")
        else:
            raise

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
