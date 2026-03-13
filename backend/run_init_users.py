from backend.modules.users.services import create_user, get_user_by_email
from backend.core.database import SessionLocal

def init_users():
    db = SessionLocal()
    if not get_user_by_email(db, "admin@farm.com"):
        create_user(db, username="admin", email="admin@farm.com", password="admin123", is_superuser=True)
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
    db.close()

if __name__ == "__main__":
    init_users()
