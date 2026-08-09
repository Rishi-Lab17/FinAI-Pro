"""
FinAI Pro
Analytics Service

Contains calculations used by the analytics dashboard.
"""

from collections import defaultdict
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_monthly_summary(
    db: Session,
    user_id: int
):
    """
    Returns income and expense totals for each month.
    """

    income_records = (
        db.query(Income)
        .filter(
            Income.user_id == user_id
        )
        .all()
    )

    expense_records = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    monthly_data = defaultdict(
        lambda: {
            "income": 0,
            "expense": 0
        }
    )

    for income in income_records:

        month_key = income.income_date.strftime(
            "%Y-%m"
        )

        monthly_data[month_key]["income"] += (
            income.amount
        )

    for expense in expense_records:

        month_key = expense.expense_date.strftime(
            "%Y-%m"
        )

        monthly_data[month_key]["expense"] += (
            expense.amount
        )

    sorted_months = sorted(
        monthly_data.keys()
    )

    return [
        {
            "month": month,

            "income": round(
                monthly_data[month]["income"],
                2
            ),

            "expense": round(
                monthly_data[month]["expense"],
                2
            ),

            "balance": round(
                monthly_data[month]["income"]
                - monthly_data[month]["expense"],
                2
            )
        }

        for month in sorted_months
    ]


def get_expense_category_summary(
    db: Session,
    user_id: int
):
    """
    Returns total spending grouped by category.
    """

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    category_totals = defaultdict(float)

    for expense in expenses:

        category_totals[
            expense.category
        ] += expense.amount

    return [
        {
            "category": category,

            "amount": round(
                amount,
                2
            )
        }

        for category, amount
        in sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )
    ]


def get_income_category_summary(
    db: Session,
    user_id: int
):
    """
    Returns total income grouped by source category.
    """

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id == user_id
        )
        .all()
    )

    category_totals = defaultdict(float)

    for income in incomes:

        category_totals[
            income.category
        ] += income.amount

    return [
        {
            "category": category,

            "amount": round(
                amount,
                2
            )
        }

        for category, amount
        in sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )
    ]


def get_analytics_summary(
    db: Session,
    user_id: int
):
    """
    Returns the main financial analytics summary.
    """

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id == user_id
        )
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    total_income = sum(
        income.amount
        for income in incomes
    )

    total_expenses = sum(
        expense.amount
        for expense in expenses
    )

    balance = (
        total_income
        - total_expenses
    )

    savings_rate = 0

    if total_income > 0:

        savings_rate = (
            balance
            / total_income
        ) * 100

    return {

        "total_income": round(
            total_income,
            2
        ),

        "total_expenses": round(
            total_expenses,
            2
        ),

        "balance": round(
            balance,
            2
        ),

        "savings_rate": round(
            max(savings_rate, 0),
            1
        )
    }


def get_current_month_summary(
    db: Session,
    user_id: int
):
    """
    Returns financial data for the current month.
    """

    current_date = datetime.now()

    current_month = current_date.month

    current_year = current_date.year

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id == user_id
        )
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    monthly_income = 0

    monthly_expenses = 0

    for income in incomes:

        if (
            income.income_date.month
            == current_month
            and
            income.income_date.year
            == current_year
        ):

            monthly_income += income.amount

    for expense in expenses:

        if (
            expense.expense_date.month
            == current_month
            and
            expense.expense_date.year
            == current_year
        ):

            monthly_expenses += expense.amount

    return {

        "income": round(
            monthly_income,
            2
        ),

        "expense": round(
            monthly_expenses,
            2
        ),

        "balance": round(
            monthly_income
            - monthly_expenses,
            2
        )
    }