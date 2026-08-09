"""
FinAI Pro
OCR Receipt Service

Extracts useful information from receipt images.
"""

import re
from datetime import datetime

import pytesseract

from PIL import Image


def extract_text_from_receipt(
    image_path: str
):
    """
    Extracts text from a receipt image.
    """

    image = Image.open(image_path)

    text = pytesseract.image_to_string(
        image
    )

    return text


def extract_amount(text: str):
    """
    Attempts to find the total amount
    from receipt text.
    """

    patterns = [

        r"total\s*[:\-]?\s*[₹Rs.]?\s*(\d+(?:\.\d{1,2})?)",

        r"amount\s*[:\-]?\s*[₹Rs.]?\s*(\d+(?:\.\d{1,2})?)",

        r"grand\s*total\s*[:\-]?\s*[₹Rs.]?\s*(\d+(?:\.\d{1,2})?)",

        r"₹\s*(\d+(?:\.\d{1,2})?)"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:

                return float(
                    match.group(1)
                )

            except ValueError:

                pass

    return None


def extract_date(text: str):
    """
    Attempts to find a date from receipt text.
    """

    patterns = [

        r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b",

        r"\b(\d{4}[/-]\d{2}[/-]\d{2})\b",

        r"\b(\d{2}[/-]\d{2}[/-]\d{2})\b"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if not match:
            continue

        value = match.group(1)

        formats = [

            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y/%m/%d",
            "%Y-%m-%d",
            "%d/%m/%y",
            "%d-%m-%y"

        ]

        for date_format in formats:

            try:

                return datetime.strptime(
                    value,
                    date_format
                ).date()

            except ValueError:

                continue

    return None


def detect_category(text: str):
    """
    Attempts to identify the expense category
    from receipt text.
    """

    text_lower = text.lower()

    category_keywords = {

        "Food": [
            "restaurant",
            "food",
            "cafe",
            "coffee",
            "pizza",
            "burger",
            "grocery",
            "supermarket",
            "bakery"
        ],

        "Shopping": [
            "shopping",
            "mall",
            "clothing",
            "fashion",
            "store",
            "retail"
        ],

        "Healthcare": [
            "hospital",
            "medical",
            "pharmacy",
            "medicine",
            "clinic"
        ],

        "Travel": [
            "flight",
            "hotel",
            "uber",
            "ola",
            "taxi",
            "travel",
            "bus",
            "train"
        ],

        "Education": [
            "college",
            "school",
            "course",
            "education",
            "book"
        ],

        "Entertainment": [
            "movie",
            "cinema",
            "game",
            "entertainment"
        ]

    }


    for category, keywords in category_keywords.items():

        for keyword in keywords:

            if keyword in text_lower:

                return category

    return "Other"


def extract_receipt_data(
    image_path: str
):
    """
    Performs complete receipt extraction.
    """

    text = extract_text_from_receipt(
        image_path
    )

    amount = extract_amount(
        text
    )

    receipt_date = extract_date(
        text
    )

    category = detect_category(
        text
    )

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    title = "Receipt Expense"

    if lines:

        title = lines[0][:100]


    return {

        "title": title,

        "amount": amount,

        "category": category,

        "expense_date": receipt_date,

        "raw_text": text

    }