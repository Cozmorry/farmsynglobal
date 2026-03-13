# backend/seed_admin.py
# Script to create an initial admin user for FarmSyn Global.

from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend import models
from backend.security import hash_password  # <-- use this

def seed_admin():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.username == "admin").first()
        if existing:
            print("✅ Admin user already exists (username=admin).")
            return
        admin = models.User(
            username="admin",
            full_name="FarmSyn Admin",
            email="admin@farmsynglobal.online",
            hashed_password=hash_password("Admin@123"),  # <-- use hash_password
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("🌱 Admin user created: username=admin / password=Admin@123")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
