# backend/test_db.py

from backend.database import SessionLocal
from backend.models.crop_management import Crop

def test_database():
    try:
        db = SessionLocal()
        print("✅ Database session created successfully!")

        # Try reading data
        crops = db.query(Crop).all()
        print(f"✅ Crop table has {len(crops)} rows.")

    except Exception as e:
        print("❌ Database connection or query failed:", e)

    finally:
        db.close()

if __name__ == "__main__":
    test_database()
