from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import ExpenseDB, UserDB

router = APIRouter(prefix="/summary", tags=["Analytics"])


@router.get("")
def get_summary(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    query = db.query(ExpenseDB).filter(
        ExpenseDB.user_id == current_user.id
    )

    total_paise = (
        query.with_entities(func.sum(ExpenseDB.amount_paise)).scalar()
        or 0
    )
    total_count = query.count()
    total_spending = total_paise / 100

    return {
        "total_spending": total_spending,
        "number_of_expenses": total_count,
        "total_amount": total_spending,
        "total_expenses": total_count,
    }


@router.get("/monthly")
def monthly_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    if not 2000 <= year <= 2100 or not 1 <= month <= 12:
        raise HTTPException(
            status_code=422,
            detail="Enter a valid year and month",
        )

    first_day = date(year, month, 1)

    next_month = (
        date(year + 1, 1, 1)
        if month == 12
        else date(year, month + 1, 1)
    )

    expenses = (
        db.query(ExpenseDB)
        .filter(
            ExpenseDB.user_id == current_user.id,
            ExpenseDB.expense_date >= first_day,
            ExpenseDB.expense_date < next_month,
        )
        .all()
    )

    total_paise = sum(expense.amount_paise for expense in expenses)

    return {
        "year": year,
        "month": month,
        "total_expenses": len(expenses),
        "total_amount": total_paise / 100,
    }


@router.get("/categories")
def category_summary(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    results = (
        db.query(
            func.min(ExpenseDB.category),
            func.sum(ExpenseDB.amount_paise),
            func.count(ExpenseDB.id),
        )
        .filter(ExpenseDB.user_id == current_user.id)
        .group_by(func.lower(ExpenseDB.category))
        .all()
    )

    return {
        "categories": [
            {
                "category": category,
                "total_amount": total_paise / 100,
                "expense_count": count,
            }
            for category, total_paise, count in results
        ]
    }