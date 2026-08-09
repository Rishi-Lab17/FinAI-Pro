"""
FinAI Pro
Expense Routes

Handles expense pages and CRUD operations.
"""

from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.expense_schema import ExpenseCreate
from app.schemas.expense_schema import ExpenseUpdate

from app.services.auth_service import get_user_by_id

from app.services.expense_service import get_all_expenses
from app.services.expense_service import get_expense_by_id
from app.services.expense_service import create_expense
from app.services.expense_service import update_expense
from app.services.expense_service import delete_expense
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


@router.get(
    "/expense",
    response_class=HTMLResponse
)
async def expense_page(
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

    expense_list = get_all_expenses(
        db,
        user.id
    )

    total_expenses = get_total_expenses(
        db,
        user.id
    )

    current_date = datetime.now()

    monthly_expenses = get_monthly_expenses(
        db,
        user.id,
        current_date.month,
        current_date.year
    )

    return templates.TemplateResponse(
        "expense.html",
        {
            "request": request,
            "user": user,
            "expense_list": expense_list,
            "total_expenses": total_expenses,
            "monthly_expenses": monthly_expenses
        }
    )


@router.get(
    "/expense/add",
    response_class=HTMLResponse
)
async def add_expense_page(
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

    return templates.TemplateResponse(
        "add_expense.html",
        {
            "request": request,
            "user": user
        }
    )


@router.post("/expense/add")
async def save_expense(

    request: Request,

    title: str = Form(...),

    category: str = Form(...),

    amount: float = Form(...),

    payment_method: str = Form(...),

    expense_date: str = Form(...),

    description: str = Form(""),

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

    expense = ExpenseCreate(

        title=title,

        category=category,

        amount=amount,

        payment_method=payment_method,

        expense_date=datetime.strptime(
            expense_date,
            "%Y-%m-%d"
        ).date(),

        description=description

    )

    create_expense(
        db,
        expense,
        user.id
    )

    return RedirectResponse(
        "/expense",
        status_code=303
    )


@router.get(
    "/expense/edit/{expense_id}",
    response_class=HTMLResponse
)
async def edit_expense_page(

    expense_id: int,

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

    expense = get_expense_by_id(
        db,
        expense_id,
        user.id
    )

    if expense is None:

        return RedirectResponse(
            "/expense",
            status_code=303
        )

    return templates.TemplateResponse(
        "edit_expense.html",
        {
            "request": request,
            "user": user,
            "expense": expense
        }
    )


@router.post(
    "/expense/edit/{expense_id}"
)
async def update_expense_record(

    expense_id: int,

    request: Request,

    title: str = Form(...),

    category: str = Form(...),

    amount: float = Form(...),

    payment_method: str = Form(...),

    expense_date: str = Form(...),

    description: str = Form(""),

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

    expense = ExpenseUpdate(

        title=title,

        category=category,

        amount=amount,

        payment_method=payment_method,

        expense_date=datetime.strptime(
            expense_date,
            "%Y-%m-%d"
        ).date(),

        description=description

    )

    update_expense(
        db,
        expense_id,
        expense,
        user.id
    )

    return RedirectResponse(
        "/expense",
        status_code=303
    )


@router.get(
    "/expense/delete/{expense_id}"
)
async def delete_expense_record(

    expense_id: int,

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

    delete_expense(
        db,
        expense_id,
        user.id
    )

    return RedirectResponse(
        "/expense",
        status_code=303
    )