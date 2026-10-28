from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class UserRegister(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )
    category: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=250)
    expense_date: date = Field(default_factory=date.today)


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: float
    category: str
    description: str
    expense_date: date
    created_at: datetime