import os
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt, JWTError

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_EXPIRES_IN_DAYS = int(os.getenv("JWT_EXPIRES_IN_DAYS", "7"))
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "aidigest_session")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False


def create_token(sub: str, email: str) -> str:
    exp = datetime.utcnow() + timedelta(days=JWT_EXPIRES_IN_DAYS)
    payload = {"sub": sub, "email": email, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except JWTError:
        return None

