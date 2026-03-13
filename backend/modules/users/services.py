# backend/modules/users/services.py
from sqlalchemy.orm import Session
from backend.modules.users.models import User
from backend.modules.farms.models import FarmMember
from backend.core.security import hash_password

def create_user(db: Session, username: str, email: str, password: str, is_superuser: bool = False) -> User:
    hashed_pw = hash_password(password)
    user = User(
        username=username,
        email=email,
        password=hashed_pw,
        is_active=True,
        is_superuser=is_superuser
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def add_user_to_farm(db: Session, user_id: int, farm_id: int, role: str) -> FarmMember:
    membership = FarmMember(user_id=user_id, farm_id=farm_id, role=role)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership

