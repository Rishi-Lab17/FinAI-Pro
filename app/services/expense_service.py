"""
FinAI Pro
Expense Service

This file contains the business logic
for expense management.
"""

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense_schema import ExpenseCreate
from app.schemas.expense_schema import ExpenseUpdate


def get_all_expenses(
    db: Session,
    user_id: int
):
    """
    Returns all expenses belonging to a user.
    """

    return (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .order_by(
            Expense.expense_date.desc()
        )
        .all()
    )


def get_expense_by_id(
    db: Session,
    expense_id: int,
    user_id: int
):
    """
    Returns one expense belonging to a user.
    """

    return (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
        .first()
    )


def create_expense(
    db: Session,
    expense: ExpenseCreate,
    user_id: int
):
    """
    Creates a new expense.
    """

    new_expense = Expense(

        user_id=user_id,

        title=expense.title,

        category=expense.category,

        amount=expense.amount,

        payment_method=expense.payment_method,

        description=expense.description,

        expense_date=expense.expense_date

    )

    db.add(new_expense)

    db.commit()

    db.refresh(new_expense)

    return new_expense


def update_expense(
    db: Session,
    expense_id: int,
    expense: ExpenseUpdate,
    user_id: int
):
    """
    Updates an existing expense.
    """

    existing_expense = get_expense_by_id(
        db,
        expense_id,
        user_id
    )

    if existing_expense is None:

        return None

    existing_expense.title = expense.title

    existing_expense.category = expense.category

    existing_expense.amount = expense.amount

    existing_expense.payment_method = expense.payment_method

    existing_expense.description = expense.description

    existing_expense.expense_date = expense.expense_date

    db.commit()

    db.refresh(existing_expense)

    return existing_expense


def delete_expense(
    db: Session,
    expense_id: int,
    user_id: int
):
    """
    Deletes an expense belonging to a user.
    """

    expense = get_expense_by_id(
        db,
        expense_id,
        user_id
    )

    if expense is None:

        return False

    db.delete(expense)

    db.commit()

    return True


def get_total_expenses(
    db: Session,
    user_id: int
):
    """
    Calculates total expenses for a user.
    """

    expense_list = get_all_expenses(
        db,
        user_id
    )

    return sum(
        item.amount
        for item in expense_list
    )


def get_monthly_expenses(
    db: Session,
    user_id: int,
    month: int,
    year: int
):
    """
    Calculates expenses for a specific month.
    """

    total = 0

    expense_list = get_all_expenses(
        db,
        user_id
    )

    for item in expense_list:

        if (
            item.expense_date.month == month
            and
            item.expense_date.year == year
        ):

            total += item.amount

    return total