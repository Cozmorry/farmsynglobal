# backend/create_test_user.py
from backend.core.database import SessionLocal
from backend.modules.users import models
from backend.core.security import get_password_hash

def create_test_user():
    db = SessionLocal()

    email = "testuser@example.com"
    password = "Password123!"  # Use a secure password
    username = "testuser"

    # Check if user already exists
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        print("Test user already exists.")
        return

    # Create new user
    user = models.User(
        username=username,
        email=email,
        password_hash=get_password_hash(password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"✅ Test user created: {email} / {password}")

if __name__ == "__main__":
    create_test_user()
