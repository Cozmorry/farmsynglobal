#backend/core/Security.py
import hashlib
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.modules.users.models import User

# Load environment variables
from dotenv import load_dotenv
import os

load_dotenv()

# ============================================================
# PASSWORD HASHING (bcrypt - widely supported)
# ============================================================
# Bcrypt 5.0+ raises on passwords > 72 bytes. We SHA256-hash first
# so the input to bcrypt is always 64 hex chars (64 bytes).
# ============================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bcrypt rejects input > 72 bytes. Truncate password first, then SHA256 -> fixed 64 bytes.
_BCRYPT_MAX_BYTES = 72


def _to_bcrypt_input(password: str) -> str:
    """Truncate password to 72 bytes, then SHA256 -> 64-char hex. Safe for any bcrypt version."""
    if not password:
        return hashlib.sha256(b"").hexdigest()
    b = password.encode("utf-8")
    if len(b) > _BCRYPT_MAX_BYTES:
        b = b[:_BCRYPT_MAX_BYTES]
        # Avoid cutting multi-byte UTF-8 in the middle
        while b and (b[-1] & 0xC0) == 0x80:
            b = b[:-1]
        password = b.decode("utf-8", errors="replace")
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    return pwd_context.hash(_to_bcrypt_input(password))


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(_to_bcrypt_input(plain), hashed)


# ============================================================
# JWT SETTINGS
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ============================================================
# GET CURRENT USER (FIXED VERSION)
# ============================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 🔥 FIX: We now correctly read user_id from token
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # 🔥 FIX: Query by ID instead of email
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception

    return user
