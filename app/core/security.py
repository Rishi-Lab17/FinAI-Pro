"""
FinAI Pro
Security Utilities

This file handles password hashing
and password verification.
"""

from passlib.context import CryptContext


# Password hashing configuration
password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Convert a plain password into a secure hash.
    """

    return password_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify whether the entered password
    matches the stored hashed password.
    """

    return password_context.verify(
        plain_password,
        hashed_password
    )