# backend/migrations/fill_active_modules.py

from backend.core.database import SessionLocal
from backend.modules.farms import models
from backend.core.module_registry import resolve_modules, PRODUCTION_MODULES

# ============================================================
# RUN THIS ONCE IN PRODUCTION TO MIGRATE OLD FARMS
# ============================================================

db = SessionLocal()

try:
    farms = db.query(models.Farm).all()
    for farm in farms:
        # Skip if active_modules already set
        if farm.active_modules:
            continue

        # Determine initial modules based on farm_type
        if farm.farm_type == models.FarmTypeEnum.mixed:
            # Mixed farm → include all production modules
            farm.active_modules = list(PRODUCTION_MODULES.keys())
        else:
            # Single-type farm → resolve dependencies
            farm.active_modules = resolve_modules([farm.farm_type.value])

        print(f"Updated farm {farm.id}: {farm.active_modules}")
        db.add(farm)

    db.commit()
    print("✅ Migration complete: all farms now have active_modules set")

finally:
    db.close()
