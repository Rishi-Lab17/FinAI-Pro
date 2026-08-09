"""
FinAI Pro
Main Application
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core.database import Base
from app.core.database import engine

from app.models.user import User
from app.models.income import Income
from app.models.expense import Expense
from app.routers.auth import router as auth_router
from app.routers.income import router as income_router
from app.routers.expense import router as expense_router
from app.routers.dashboard import router as dashboard_router
from app.routers.analytics import router as analytics_router
from app.routers.ai_advisor import router as ai_advisor_router
from app.routers.ai_challenge import router as ai_challenge_router
from app.routers.ocr import router as ocr_router
from app.routers.profile import router as profile_router
# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION
)


# =========================================================
# SESSION
# =========================================================

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static"
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(
    auth_router
)

app.include_router(
    income_router
)

app.include_router(
    expense_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    analytics_router
)

app.include_router(
    ai_advisor_router
)

app.include_router(
    ai_challenge_router
)

app.include_router(
    ocr_router
)

app.include_router(
    profile_router
)
# =========================================================
# HOME
# =========================================================

@app.get(
    "/",
    include_in_schema=False
)
async def home():

    return RedirectResponse(
        "/login"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "running",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }


# =========================================================
# TEST
# =========================================================

@app.get("/test")
async def test():

    return HTMLResponse(
        """
        <!DOCTYPE html>

        <html>

        <head>
            <title>FinAI Pro Test</title>
        </head>

        <body>

            <h1>FinAI Pro Test</h1>

            <p>
                FastAPI HTML is working.
            </p>

        </body>

        </html>
        """
    )
