from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.modules.farms.models import Farm, Block, Greenhouse, Barn, Coop, Pond

def check_invalid_json_fields(db: Session):
    # Check Farms
    farms = db.query(Farm).all()
    for farm in farms:
        try:
            # Validate size field in Farm
            if isinstance(farm.size, dict) and ("value" in farm.size and "unit" in farm.size):
                value = farm.size.get("value")
                unit = farm.size.get("unit")
                if not isinstance(value, (int, float)) or not isinstance(unit, str):
                    print(f"Invalid size in Farm {farm.id}: {farm.size}")
            else:
                print(f"Missing or malformed size field in Farm {farm.id}: {farm.size}")
        except Exception as e:
            print(f"Error checking Farm {farm.id}: {str(e)}")

        # Validate Blocks, Greenhouses, etc.
        for structure in [farm.blocks, farm.greenhouses, farm.barns, farm.coops, farm.ponds]:
            for obj in structure:
                try:
                    if hasattr(obj, "area") and isinstance(obj.area, dict):
                        if "value" in obj.area and "unit" in obj.area:
                            value = obj.area.get("value")
                            unit = obj.area.get("unit")
                            if not isinstance(value, (int, float)) or not isinstance(unit, str):
                                print(f"Invalid area in {obj.__class__.__name__} {obj.id}: {obj.area}")
                        else:
                            print(f"Missing or malformed area field in {obj.__class__.__name__} {obj.id}: {obj.area}")
                except Exception as e:
                    print(f"Error checking {obj.__class__.__name__} {obj.id}: {str(e)}")

# Call the function to check all farms and structures
if __name__ == "__main__":
    db = next(get_db())  # Get your database session (ensure it's a session, not a generator)
    check_invalid_json_fields(db)
