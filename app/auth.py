
from datetime import datetime, timedelta, timezone
import os
import re

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserDB


load_dotenv()

SECRET_KEY = os.getenv("SPENDWISE_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SPENDWISE_SECRET_KEY is missing. "
        "Add it to your .env file before starting SpendWise."
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30

password_hasher = PasswordHash.recommended()
security = HTTPBearer()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)


def normalize_email(email: str) -> str:
    email = email.strip().lower()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise HTTPException(
            status_code=422,
            detail="Enter a valid email address",
        )

    return email


def create_access_token(user_id: int, email: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_MINUTES
    )

    return jwt.encode(
        {
            "sub": str(user_id),
            "email": email,
            "exp": expires_at,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserDB:
    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        subject = payload.get("sub")
        if not subject:
            raise unauthorized

        user_id = int(subject)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise unauthorized

    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if user is None:
        raise unauthorized

    return user
