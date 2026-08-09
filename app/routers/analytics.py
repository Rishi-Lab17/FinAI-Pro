"""
FinAI Pro
Analytics Routes

Handles the financial analytics dashboard.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.auth_service import get_user_by_id

from app.services.analytics_service import (
    get_analytics_summary,
    get_current_month_summary,
    get_monthly_summary,
    get_expense_category_summary,
    get_income_category_summary
)


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
    "/analytics",
    response_class=HTMLResponse
)
async def analytics_page(
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

    summary = get_analytics_summary(
        db,
        user.id
    )

    current_month = get_current_month_summary(
        db,
        user.id
    )

    monthly_summary = get_monthly_summary(
        db,
        user.id
    )

    expense_categories = get_expense_category_summary(
        db,
        user.id
    )

    income_categories = get_income_category_summary(
        db,
        user.id
    )

    return templates.TemplateResponse(
        "analytics.html",
        {
            "request": request,
            "user": user,
            "summary": summary,
            "current_month": current_month,
            "monthly_summary": monthly_summary,
            "expense_categories": expense_categories,
            "income_categories": income_categories
        }
    )