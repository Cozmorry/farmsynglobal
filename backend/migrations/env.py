# backend/migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# ------------------------------------------------------
# 1️⃣ Add project root to sys.path
# ------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# ------------------------------------------------------
# 2️⃣ Import Base + all modules/models
# ------------------------------------------------------
from backend.core.database import Base

# Modules
import backend.modules.agronomy.models
import backend.modules.aquaculture.models
import backend.modules.crop_management.models
import backend.modules.farms.models
import backend.modules.finance.models
import backend.modules.hr.models
import backend.modules.livestock.models
import backend.modules.poultry.models
import backend.modules.store_inventory.models
import backend.modules.users.models
import backend.modules.veterinary.models
import backend.modules.weather.models
import backend.modules.audit.models
import backend.modules.tenants.models


# ------------------------------------------------------
# 3️⃣ Alembic config
# ------------------------------------------------------
config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# ------------------------------------------------------
# ⭐ Include all objects (safe)
# ------------------------------------------------------
def include_object(object_, name, type_, reflected, compare_to):
    return True

# ------------------------------------------------------
# 4️⃣ Offline migrations
# ------------------------------------------------------
def run_migrations_offline():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("Environment variable DATABASE_URL is not set")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_object=include_object,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ------------------------------------------------------
# 5️⃣ Online migrations
# ------------------------------------------------------
def run_migrations_online():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("Environment variable DATABASE_URL is not set")

    connectable = engine_from_config(
        {"sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# ------------------------------------------------------
# 6️⃣ Run migrations
# ------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
