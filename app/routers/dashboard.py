"""
FinAI Pro
Dashboard Routes
"""

from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.auth_service import get_user_by_id

from app.services.income_service import get_all_income
from app.services.income_service import get_total_income
from app.services.income_service import get_monthly_income

from app.services.expense_service import get_all_expenses
from app.services.expense_service import get_total_expenses
from app.services.expense_service import get_monthly_expenses


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


def get_current_user(
    request: Request,
    db: Session
):

    user_id = request.session.get("user_id")

    if user_id is None:
        return None

    return get_user_by_id(
        db,
        user_id
    )


def get_time_greeting():

    current_hour = datetime.now().hour

    if current_hour < 12:
        return "Good morning"

    if current_hour < 17:
        return "Good afternoon"

    return "Good evening"


def calculate_financial_health(
    total_income,
    total_expenses
):

    if total_income <= 0:
        return 0

    savings_rate = (
        (total_income - total_expenses)
        / total_income
    ) * 100

    if savings_rate >= 40:
        return 95

    if savings_rate >= 30:
        return 90

    if savings_rate >= 20:
        return 80

    if savings_rate >= 10:
        return 70

    if savings_rate > 0:
        return 60

    return 35


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard_page(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_current_user(
        request,
        db
    )

    if user is None:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    current_date = datetime.now()

    total_income = get_total_income(
        db,
        user.id
    )

    total_expenses = get_total_expenses(
        db,
        user.id
    )

    current_balance = (
        total_income - total_expenses
    )

    monthly_income = get_monthly_income(
        db,
        user.id,
        current_date.month,
        current_date.year
    )

    monthly_expenses = get_monthly_expenses(
        db,
        user.id,
        current_date.month,
        current_date.year
    )

    monthly_balance = (
        monthly_income - monthly_expenses
    )

    if total_income > 0:

        savings_rate = (
            current_balance / total_income
        ) * 100

    else:

        savings_rate = 0

    if savings_rate < 0:
        savings_rate = 0

    financial_health = calculate_financial_health(
        total_income,
        total_expenses
    )

    all_income = get_all_income(
        db,
        user.id
    )

    all_expenses = get_all_expenses(
        db,
        user.id
    )

    recent_transactions = []

    for income in all_income[:5]:

        recent_transactions.append({

            "type": "income",

            "title": income.source,

            "category": income.category,

            "amount": income.amount,

            "date": income.income_date

        })

    for expense in all_expenses[:5]:

        recent_transactions.append({

            "type": "expense",

            "title": expense.title,

            "category": expense.category,

            "amount": expense.amount,

            "date": expense.expense_date

        })

    recent_transactions.sort(
        key=lambda item: item["date"],
        reverse=True
    )

    recent_transactions = recent_transactions[:8]

    greeting = get_time_greeting()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "greeting": greeting,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "current_balance": current_balance,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "monthly_balance": monthly_balance,
            "savings_rate": round(
                savings_rate,
                1
            ),
            "financial_health": financial_health,
            "recent_transactions": recent_transactions
        }
    )