from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import ExpenseDB, UserDB
from app.schemas import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def amount_to_paise(amount: Decimal) -> int:
    return int(amount * 100)


def clean_text(value: str, field_name: str) -> str:
    value = value.strip()

    if not value:
        raise HTTPException(
            status_code=422,
            detail=f"{field_name} cannot be empty",
        )

    return value


def find_owned_expense(
    db: Session,
    expense_id: int,
    user_id: int,
) -> ExpenseDB:
    expense = (
        db.query(ExpenseDB)
        .filter(
            ExpenseDB.id == expense_id,
            ExpenseDB.user_id == user_id,
        )
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return expense


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    expense = ExpenseDB(
        user_id=current_user.id,
        amount_paise=amount_to_paise(data.amount),
        category=clean_text(data.category, "Category"),
        description=clean_text(data.description, "Description"),
        expense_date=data.expense_date,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.get("", response_model=list[ExpenseResponse])
def list_expenses(
    category: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="start_date must be on or before end_date",
        )

    query = db.query(ExpenseDB).filter(
        ExpenseDB.user_id == current_user.id
    )

    if category:
        query = query.filter(
            func.lower(ExpenseDB.category) == category.strip().lower()
        )

    if start_date:
        query = query.filter(ExpenseDB.expense_date >= start_date)

    if end_date:
        query = query.filter(ExpenseDB.expense_date <= end_date)

    return query.order_by(
        ExpenseDB.expense_date.desc(),
        ExpenseDB.id.desc(),
    ).all()


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    return find_owned_expense(db, expense_id, current_user.id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    expense = find_owned_expense(db, expense_id, current_user.id)

    expense.amount_paise = amount_to_paise(data.amount)
    expense.category = clean_text(data.category, "Category")
    expense.description = clean_text(data.description, "Description")
    expense.expense_date = data.expense_date

    db.commit()
    db.refresh(expense)

    return expense


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    expense = find_owned_expense(db, expense_id, current_user.id)

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully",
        "expense_id": expense_id,
    }