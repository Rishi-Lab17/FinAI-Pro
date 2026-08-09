"""
FinAI Pro
Authentication Routes

Handles:
- Login
- Registration
- Logout
- Account validation
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

from app.schemas.user_schema import UserRegister

from app.services.auth_service import authenticate_user
from app.services.auth_service import create_user
from app.services.auth_service import get_user_by_email


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


# ============================================================
# LOGIN PAGE
# ============================================================

@router.get(
    "/login",
    response_class=HTMLResponse
)
async def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
            "user": None,
            "error": None,
            "error_title": None,
            "account_not_found": False,
            "email": ""
        }
    )


# ============================================================
# REGISTER PAGE
# ============================================================

@router.get(
    "/register",
    response_class=HTMLResponse
)
async def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request,
            "user": None,
            "error": None
        }
    )


# ============================================================
# REGISTER USER
# ============================================================

@router.post(
    "/register",
    response_class=HTMLResponse
)
async def register_user(

    request: Request,

    full_name: str = Form(...),

    email: str = Form(...),

    password: str = Form(...),

    confirm_password: str = Form(...),

    db: Session = Depends(get_db)

):

    # --------------------------------------------------------
    # CLEAN INPUT
    # --------------------------------------------------------

    full_name = full_name.strip()

    email = email.strip().lower()


    # --------------------------------------------------------
    # VALIDATE NAME
    # --------------------------------------------------------

    if len(full_name) < 2:

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "request": request,
                "user": None,
                "error":
                    "Name must contain at least 2 characters."
            }
        )


    # --------------------------------------------------------
    # VALIDATE EMAIL
    # --------------------------------------------------------

    if "@" not in email:

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "request": request,
                "user": None,
                "error":
                    "Please enter a valid email address."
            }
        )


    # --------------------------------------------------------
    # VALIDATE PASSWORD
    # --------------------------------------------------------

    if len(password) < 6:

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "request": request,
                "user": None,
                "error":
                    "Password must contain at least 6 characters."
            }
        )


    # --------------------------------------------------------
    # CONFIRM PASSWORD
    # --------------------------------------------------------

    if password != confirm_password:

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "request": request,
                "user": None,
                "error":
                    "Passwords do not match."
            }
        )


    # --------------------------------------------------------
    # CREATE USER SCHEMA
    # --------------------------------------------------------

    user_data = UserRegister(

        full_name=full_name,

        email=email,

        password=password

    )


    # --------------------------------------------------------
    # CREATE DATABASE USER
    # --------------------------------------------------------

    created_user = create_user(
        db,
        user_data
    )


    # --------------------------------------------------------
    # DUPLICATE EMAIL
    # --------------------------------------------------------

    if created_user is None:

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "request": request,
                "user": None,
                "error":
                    "An account with this email already exists."
            }
        )


    # --------------------------------------------------------
    # REGISTRATION SUCCESS
    # --------------------------------------------------------

    return RedirectResponse(
        "/login",
        status_code=303
    )


# ============================================================
# LOGIN USER
# ============================================================

@router.post(
    "/login",
    response_class=HTMLResponse
)
async def login_user(

    request: Request,

    email: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db)

):

    # --------------------------------------------------------
    # CLEAN EMAIL
    # --------------------------------------------------------

    email = email.strip().lower()


    # --------------------------------------------------------
    # CHECK WHETHER ACCOUNT EXISTS
    # --------------------------------------------------------

    existing_user = get_user_by_email(
        db,
        email
    )


    # --------------------------------------------------------
    # ACCOUNT DOES NOT EXIST
    # --------------------------------------------------------

    if existing_user is None:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={

                "request": request,

                "user": None,

                "error_title":
                    "Account Not Found",

                "error":
                    "No account exists with this email. "
                    "Please create an account first.",

                "account_not_found":
                    True,

                "email":
                    email

            }
        )


    # --------------------------------------------------------
    # AUTHENTICATE PASSWORD
    # --------------------------------------------------------

    user = authenticate_user(

        db,

        email,

        password

    )


    # --------------------------------------------------------
    # WRONG PASSWORD
    # --------------------------------------------------------

    if user is None:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={

                "request": request,

                "user": None,

                "error_title":
                    "Incorrect Password",

                "error":
                    "The password you entered is incorrect. "
                    "Please try again.",

                "account_not_found":
                    False,

                "email":
                    email

            }
        )


    # --------------------------------------------------------
    # CHECK ACCOUNT STATUS
    # --------------------------------------------------------

    if not user.is_active:

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={

                "request": request,

                "user": None,

                "error_title":
                    "Account Inactive",

                "error":
                    "Your account is currently inactive.",

                "account_not_found":
                    False,

                "email":
                    email

            }
        )


    # --------------------------------------------------------
    # CLEAR OLD SESSION
    # --------------------------------------------------------

    request.session.clear()


    # --------------------------------------------------------
    # STORE LOGGED-IN USER ID
    # --------------------------------------------------------

    request.session["user_id"] = user.id


    # --------------------------------------------------------
    # REDIRECT TO DASHBOARD
    # --------------------------------------------------------

    return RedirectResponse(
        "/dashboard",
        status_code=303
    )


# ============================================================
# LOGOUT
# ============================================================

@router.get(
    "/logout"
)
async def logout_user(
    request: Request
):

    # Only clear the session.
    #
    # IMPORTANT:
    # This does NOT delete the user's database records.

    request.session.clear()


    return RedirectResponse(
        "/login",
        status_code=303
    )