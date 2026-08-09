"""
FinAI Pro
Income Service
"""

from datetime import date

from sqlalchemy.orm import Session

from app.models.income import Income
from app.schemas.income_schema import IncomeCreate
from app.schemas.income_schema import IncomeUpdate


def get_all_income(db: Session, user_id: int):

    return (
        db.query(Income)
        .filter(Income.user_id == user_id)
        .order_by(Income.income_date.desc())
        .all()
    )


def get_income_by_id(
    db: Session,
    income_id: int,
    user_id: int
):

    return (
        db.query(Income)
        .filter(
            Income.id == income_id,
            Income.user_id == user_id
        )
        .first()
    )


def create_income(
    db: Session,
    income: IncomeCreate,
    user_id: int
):

    new_income = Income(

        user_id=user_id,

        source=income.source,

        category=income.category,

        amount=income.amount,

        description=income.description,

        income_date=income.income_date

    )

    db.add(new_income)

    db.commit()

    db.refresh(new_income)

    return new_income


def update_income(
    db: Session,
    income_id: int,
    income: IncomeUpdate,
    user_id: int
):

    existing_income = get_income_by_id(
        db,
        income_id,
        user_id
    )

    if existing_income is None:

        return None

    existing_income.source = income.source

    existing_income.category = income.category

    existing_income.amount = income.amount

    existing_income.description = income.description

    existing_income.income_date = income.income_date

    db.commit()

    db.refresh(existing_income)

    return existing_income


def delete_income(
    db: Session,
    income_id: int,
    user_id: int
):

    income = get_income_by_id(
        db,
        income_id,
        user_id
    )

    if income is None:

        return False

    db.delete(income)

    db.commit()

    return True


def get_total_income(
    db: Session,
    user_id: int
):

    income_list = get_all_income(
        db,
        user_id
    )

    return sum(
        item.amount
        for item in income_list
    )


def get_monthly_income(
    db: Session,
    user_id: int,
    month: int,
    year: int
):

    total = 0

    income_list = get_all_income(
        db,
        user_id
    )

    for item in income_list:

        if (
            item.income_date.month == month
            and
            item.income_date.year == year
        ):

            total += item.amount

    return total