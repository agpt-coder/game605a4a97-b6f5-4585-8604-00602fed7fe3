from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    Response model for a user's profile information, including nickname, avatar URL, and potentially other personalization settings.
    """

    nickname: str
    avatarUrl: str
    email: str
    createdAt: datetime
    updatedAt: datetime


async def get_user_profile() -> UserProfileResponse:
    """
    Retrieve the user's profile information.

    This function fetches a user's profile information, including nickname, avatar URL, and other personalization settings.
    It queries the database for the User and associated UserProfile. The function assumes there is a mechanism
    in place to identify the current user, for example, extracting the user ID from a session or a token.

    Returns:
        UserProfileResponse: Response model for a user's profile information.
    """
    current_user_id = "some_user_id"
    user_profile = await prisma.models.UserProfile.prisma().find_unique(
        where={"userId": current_user_id}, include={"user": True}
    )
    if user_profile is None or user_profile.user is None:
        raise Exception("User profile could not be found.")
    response = UserProfileResponse(
        nickname=user_profile.nickname,
        avatarUrl=user_profile.avatarUrl or "",
        email=user_profile.user.email,
        createdAt=user_profile.createdAt,
        updatedAt=user_profile.updatedAt,
    )
    return response
