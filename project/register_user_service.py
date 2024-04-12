from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    This model represents the response after attempting to register a new user. Contains success status and user information if registration is successful.
    """

    success: bool
    user_id: Optional[str] = None
    error: Optional[str] = None


async def register_user(email: str, password: str) -> RegisterUserResponse:
    """
    Register a new user account.

    Args:
    email (str): The email address for the new user account. Must be unique and valid.
    password (str): The password for the new user account. It will be hashed before storage for security.

    Returns:
    RegisterUserResponse: This model represents the response after attempting to register a new user. Contains success status and user information if registration is successful.
    """
    user = await prisma.models.User.prisma().find_first(where={"email": email})
    if user:
        return RegisterUserResponse(success=False, error="Email already in use")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    try:
        new_user = await prisma.models.User.prisma().create(
            data={"email": email, "hashedPassword": hashed_password}
        )
        return RegisterUserResponse(success=True, user_id=new_user.id)
    except Exception as e:
        return RegisterUserResponse(success=False, error=str(e))
