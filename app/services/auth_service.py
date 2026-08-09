"""
FinAI Pro
Authentication Service

This file contains all authentication related
business logic.
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserRegister
from app.core.security import hash_password
from app.core.security import verify_password


def get_user_by_email(db: Session, email: str):

    """
    Returns a user by email.
    """

    return db.query(User).filter(
        User.email == email
    ).first()


def get_user_by_id(db: Session, user_id: int):

    """
    Returns a user by ID.
    """

    return db.query(User).filter(
        User.id == user_id
    ).first()


def create_user(db: Session, user: UserRegister):

    """
    Creates a new user.
    """

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        return None

    new_user = User(

        full_name=user.full_name,

        email=user.email,

        password=hash_password(user.password)

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    """
    Verifies login credentials.
    """

    user = get_user_by_email(
        db,
        email
    )

    if user is None:

        return None

    if not verify_password(
        password,
        user.password
    ):

        return None

    return user


def update_profile(
    db: Session,
    user: User,
    full_name: str,
    profile_image: str
):

    """
    Updates user profile.
    """

    user.full_name = full_name

    user.profile_image = profile_image

    db.commit()

    db.refresh(user)

    return user


def change_password(
    db: Session,
    user: User,
    new_password: str
):

    """
    Updates user password.
    """

    user.password = hash_password(
        new_password
    )

    db.commit()

    db.refresh(user)

    return user