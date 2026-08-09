"""
FinAI Pro
User Schemas

These schemas validate user data
for API requests and responses.
"""

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserRegister(BaseModel):
    """
    Schema for user registration.
    """

    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login.
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Schema returned to the frontend.
    """

    id: int
    full_name: str
    email: EmailStr
    profile_image: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """
    Schema for updating profile.
    """

    full_name: str
    profile_image: str


class ChangePassword(BaseModel):
    """
    Schema for changing password.
    """

    current_password: str
    new_password: str