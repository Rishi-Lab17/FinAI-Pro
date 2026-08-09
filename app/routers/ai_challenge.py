"""
FinAI Pro
AI Challenge Routes

Displays personalized financial challenges
and handles challenge completion.
"""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import get_user_by_id
from app.services.ai_challenge_service import get_ai_challenges


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
    "/ai-challenge",
    response_class=HTMLResponse
)
async def ai_challenge_page(
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

    result = get_ai_challenges(
        db,
        user.id
    )

    completed_challenges = request.session.get(
        "completed_challenges",
        []
    )

    return templates.TemplateResponse(
        "ai_challenge.html",
        {
            "request": request,
            "user": user,
            "profile": result.get(
                "profile",
                {}
            ),
            "challenges": result.get(
                "challenges",
                []
            ),
            "completed_challenges":
                completed_challenges
        }
    )


@router.post(
    "/ai-challenge/complete"
)
async def complete_challenge(
    request: Request,
    challenge_title: str = Form(...),
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

    challenge_title = challenge_title.strip()

    if not challenge_title:
        return RedirectResponse(
            "/ai-challenge",
            status_code=303
        )

    completed_challenges = request.session.get(
        "completed_challenges",
        []
    )

    if challenge_title not in completed_challenges:
        completed_challenges.append(
            challenge_title
        )

    completed_challenges = completed_challenges[-20:]

    request.session[
        "completed_challenges"
    ] = completed_challenges

    return RedirectResponse(
        "/ai-challenge",
        status_code=303
    )