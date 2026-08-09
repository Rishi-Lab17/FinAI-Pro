"""
FinAI Pro
AI Financial Advisor Routes

Handles the AI-powered financial advisor page.
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

from app.services.ai_advisor_service import (
    get_ai_financial_advice
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
    "/ai-advisor",
    response_class=HTMLResponse
)
async def ai_advisor_page(
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


    advisor_result = get_ai_financial_advice(
        db,
        user.id
    )


    financial_data = advisor_result[
        "financial_data"
    ]

    advice = advisor_result[
        "advice"
    ]


    return templates.TemplateResponse(
        "ai_advisor.html",
        {
            "request": request,
            "user": user,
            "financial_data": financial_data,
            "advice": advice
        }
    )