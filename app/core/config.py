"""
FinAI Pro
Application Configuration
"""

from pathlib import Path


class Settings:
    """Application settings."""

    PROJECT_NAME = "FinAI Pro"

    PROJECT_DESCRIPTION = (
        "AI Powered Personal Finance Management System"
    )

    PROJECT_VERSION = "1.0.0"

    BASE_DIR = (
        Path(__file__)
        .resolve()
        .parent
        .parent
        .parent
    )

    DATABASE_DIR = BASE_DIR / "database"

    DATABASE_URL = (
        f"sqlite:///{DATABASE_DIR / 'finai.db'}"
    )

    SECRET_KEY = (
        "finai_pro_secret_key_change_this_before_deployment"
    )

    UPLOAD_FOLDER = (
        BASE_DIR
        / "app"
        / "static"
        / "uploads"
    )

    REPORTS_FOLDER = (
        BASE_DIR / "reports"
    )

    DEBUG = True


settings = Settings()


settings.DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

settings.UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

settings.REPORTS_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)