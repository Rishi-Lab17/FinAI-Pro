"""
FinAI Pro
Profile Routes
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.auth_service import get_user_by_id
from app.services.auth_service import update_profile
from app.services.auth_service import change_password


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
    "/profile",
    response_class=HTMLResponse
)
async def profile_page(
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
        "profile.html",
        {
            "request": request,
            "user": user
        }
    )


@router.post("/profile/update")
async def update_user_profile(

    request: Request,

    full_name: str = Form(...),

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

    update_profile(
        db,
        user,
        full_name,
        user.profile_image
    )

    return RedirectResponse(
        "/profile",
        status_code=303
    )


@router.post("/profile/password")
async def update_user_password(

    request: Request,

    current_password: str = Form(...),

    new_password: str = Form(...),

    confirm_password: str = Form(...),

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

    if new_password != confirm_password:

        return RedirectResponse(
            "/profile",
            status_code=303
        )

    if len(new_password) < 6:

        return RedirectResponse(
            "/profile",
            status_code=303
        )

    from app.core.security import verify_password

    if not verify_password(
        current_password,
        user.password
    ):

        return RedirectResponse(
            "/profile",
            status_code=303
        )

    change_password(
        db,
        user,
        new_password
    )

    return RedirectResponse(
        "/profile",
        status_code=303
    )