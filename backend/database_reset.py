"""
Utility script to reset the database schema.
Use this ONLY in development — it drops and recreates all tables.
"""

from backend.database import Base, engine
from backend.models import crop_management, farm  # 👈 import all your models

def reset_database():
    print("⚠️ Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    print("🧱 Recreating all tables...")
    Base.metadata.create_all(bind=engine)

    print("✅ Database has been reset successfully!")

if __name__ == "__main__":
    reset_database()
