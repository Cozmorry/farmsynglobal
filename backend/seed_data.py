from datetime import date
from backend.database import SessionLocal
from backend.models.crop_management import Crop, CropBlock
from backend.models.farm import Farm, Block  # ✅ Corrected import

def seed_data():
    db = SessionLocal()
    try:
        print("🚜 Starting data seeding...")

        # 1️⃣ Create a demo farm
        demo_farm = Farm(
            name="FarmSyn Demo Farm",
            location="Demo City",
            size="50 acres",
            farm_type="crop",   # required field in your model
            owner_id=1          # temporary owner (can be adjusted)
        )
        db.add(demo_farm)
        db.commit()
        db.refresh(demo_farm)
        print(f"✅ Created Farm: {demo_farm.name}")

        # 2️⃣ Create a block
        block_a = Block(name="Block A", farm_id=demo_farm.id)
        db.add(block_a)
        db.commit()
        db.refresh(block_a)
        print(f"✅ Created Block: {block_a.name}")

        # 3️⃣ Create a crop
        crop = Crop(
            name="Tomato",
            variety="Cherry",
            farm_id=demo_farm.id,
            greenhouse=True,
            planting_date=date.today()  # ✅ Valid field
        )
        db.add(crop)
        db.commit()
        db.refresh(crop)
        print(f"✅ Created Crop: {crop.name}")

        # 4️⃣ Link crop to block
        crop_block = CropBlock(block_id=block_a.id, crop_id=crop.id)
        db.add(crop_block)
        db.commit()
        print(f"✅ Linked {crop.name} to {block_a.name}")

    except Exception as e:
        print(f"❌ Error while seeding data: {e}")
        db.rollback()
    finally:
        db.close()
        print("🔒 Database session closed.")


if __name__ == "__main__":
    seed_data()
