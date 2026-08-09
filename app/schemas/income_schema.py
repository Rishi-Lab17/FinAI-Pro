"""
FinAI Pro
Income Schemas
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class IncomeBase(BaseModel):

    source: str = Field(
        min_length=2,
        max_length=100
    )

    amount: float = Field(
        gt=0
    )

    category: str = Field(
        min_length=2,
        max_length=50
    )

    income_date: date

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )


class IncomeCreate(IncomeBase):
    pass


class IncomeUpdate(IncomeBase):
    pass


class IncomeResponse(IncomeBase):

    id: int

    user_id: int

    class Config:
        from_attributes = True