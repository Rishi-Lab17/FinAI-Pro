"""
FinAI Pro
Income Routes
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
from app.schemas.income_schema import IncomeCreate
from app.schemas.income_schema import IncomeUpdate
from app.services.auth_service import get_user_by_id

from app.services.income_service import (
    get_all_income,
    get_income_by_id,
    create_income,
    update_income,
    delete_income
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


def current_user(request: Request, db: Session):

    user_id = request.session.get("user_id")

    if user_id is None:
        return None

    return get_user_by_id(
        db,
        user_id
    )


@router.get(
    "/income",
    response_class=HTMLResponse
)
async def income_page(
    request: Request,
    db: Session = Depends(get_db)
):

    user = current_user(request, db)

    if user is None:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    income_list = get_all_income(
        db,
        user.id
    )

    return templates.TemplateResponse(
        "income.html",
        {
            "request": request,
            "user": user,
            "income_list": income_list
        }
    )


@router.get(
    "/income/add",
    response_class=HTMLResponse
)
async def add_income_page(
    request: Request,
    db: Session = Depends(get_db)
):

    user = current_user(request, db)

    if user is None:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        "add_income.html",
        {
            "request": request,
            "user": user
        }
    )


@router.post("/income/add")
async def save_income(

    request: Request,

    source: str = Form(...),

    category: str = Form(...),

    amount: float = Form(...),

    income_date: str = Form(...),

    description: str = Form(""),

    db: Session = Depends(get_db)

):

    user = current_user(request, db)

    if user is None:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    income = IncomeCreate(

        source=source,

        category=category,

        amount=amount,

        income_date=datetime.strptime(
            income_date,
            "%Y-%m-%d"
        ).date(),

        description=description

    )

    create_income(
        db,
        income,
        user.id
    )

    return RedirectResponse(
        "/income",
        status_code=303
    )
@router.get("/income/edit/{income_id}", response_class=HTMLResponse)
async def edit_income_page(

    income_id: int,

    request: Request,

    db: Session = Depends(get_db)

):

    user = current_user(request, db)

    if user is None:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    income = get_income_by_id(
        db,
        income_id,
        user.id
    )

    if income is None:

        return RedirectResponse(
            "/income",
            status_code=303
        )

    return templates.TemplateResponse(

        "edit_income.html",

        {

            "request": request,

            "user": user,

            "income": income

        }

    )


@router.post("/income/edit/{income_id}")
async def update_income_record(

    income_id: int,

    request: Request,

    source: str = Form(...),

    category: str = Form(...),

    amount: float = Form(...),

    income_date: str = Form(...),

    description: str = Form(""),

    db: Session = Depends(get_db)

):

    user = current_user(request, db)

    if user is None:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    income = IncomeUpdate(

        source=source,

        category=category,

        amount=amount,

        income_date=datetime.strptime(
            income_date,
            "%Y-%m-%d"
        ).date(),

        description=description

    )

    update_income(

        db,

        income_id,

        income,

        user.id

    )

    return RedirectResponse(

        "/income",

        status_code=303

    )


@router.get("/income/delete/{income_id}")
async def delete_income_record(

    income_id: int,

    request: Request,

    db: Session = Depends(get_db)

):

    user = current_user(request, db)

    if user is None:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    delete_income(

        db,

        income_id,

        user.id

    )

    return RedirectResponse(

        "/income",

        status_code=303

    )    