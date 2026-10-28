from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import (
    ACCESS_TOKEN_MINUTES,
    create_access_token,
    hash_password,
    normalize_email,
    verify_password,
)
from app.database import get_db
from app.models import UserDB
from app.schemas import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    email = normalize_email(data.email)

    user = UserDB(
        email=email,
        password_hash=hash_password(data.password),
    )
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists",
        )

    return user


@router.post("/login", response_model=TokenResponse)
def login_user(
    data: UserLogin,
    db: Session = Depends(get_db),
):
    email = normalize_email(data.email)

    user = db.query(UserDB).filter(UserDB.email == email).first()

    if not user or not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_access_token(user.id, user.email),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_MINUTES * 60,
    }