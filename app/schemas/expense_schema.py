"""
FinAI Pro
Expense Schemas

These schemas validate expense data
for API requests and responses.
"""

from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ExpenseCreate(BaseModel):
    """
    Schema for creating a new expense.
    """

    title: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    amount: float = Field(..., gt=0)
    payment_method: str = Field(..., min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    expense_date: date


class ExpenseUpdate(BaseModel):
    """
    Schema for updating an expense.
    """

    title: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    amount: float = Field(..., gt=0)
    payment_method: str = Field(..., min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    expense_date: date


class ExpenseResponse(BaseModel):
    """
    Schema returned to the frontend.
    """

    id: int
    user_id: int
    title: str
    category: str
    amount: float
    payment_method: str
    description: str | None
    expense_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)