"""
FinAI Pro
OCR Receipt Routes
"""

import os
import uuid

from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import Request
from fastapi import UploadFile

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

from app.services.auth_service import get_user_by_id

from app.services.ocr_service import extract_receipt_data

from app.schemas.expense_schema import ExpenseCreate
from app.services.expense_service import create_expense


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
    "/ocr",
    response_class=HTMLResponse
)
async def ocr_page(
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
        "ocr.html",
        {
            "request": request,
            "user": user
        }
    )


@router.post(
    "/ocr",
    response_class=HTMLResponse
)
async def process_receipt(
    request: Request,
    file: UploadFile = File(...),
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


    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }


    original_name = file.filename or ""

    extension = os.path.splitext(
        original_name
    )[1].lower()


    if extension not in allowed_extensions:

        return templates.TemplateResponse(
            "ocr.html",
            {
                "request": request,
                "user": user,
                "error":
                    "Please upload a JPG, JPEG, PNG or WEBP image."
            }
        )


    os.makedirs(
        settings.UPLOAD_FOLDER,
        exist_ok=True
    )


    unique_name = (
        f"{uuid.uuid4()}{extension}"
    )


    file_path = (
        settings.UPLOAD_FOLDER
        / unique_name
    )


    file_content = await file.read()


    with open(
        file_path,
        "wb"
    ) as output_file:

        output_file.write(
            file_content
        )


    try:

        receipt_data = extract_receipt_data(
            str(file_path)
        )

    except Exception as error:

        print(
            "OCR ERROR:",
            error
        )

        return templates.TemplateResponse(
            "ocr.html",
            {
                "request": request,
                "user": user,
                "error":
                    "Unable to process the receipt. Please try another image."
            }
        )


    return templates.TemplateResponse(
        "ocr.html",
        {
            "request": request,
            "user": user,
            "receipt_data": receipt_data
        }
    )


@router.post(
    "/ocr/add-expense"
)
async def add_ocr_expense(

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