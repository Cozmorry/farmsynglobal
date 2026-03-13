# backend/create_admin.py

from backend.database import SessionLocal
from backend.models.user import User
from backend.utils import get_password_hash  # Importing the function correctly

db = SessionLocal()

# Hash the password using the get_password_hash function
hashed_password = get_password_hash("admin123")  # Your password

# Create the admin user
admin = User(
    username="Kombo",
    email="kombo@gmail.com",
    password=hashed_password,
    is_active=True,
    is_superuser=True
)

# Add the admin to DB
db.add(admin)
db.commit()
db.close()

print("Admin user created successfully!")
