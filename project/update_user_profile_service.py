from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CharacterConfigUpdate(BaseModel):
    """
    Defines the fields available for updating a character's configuration, including appearance, abilities, and backstory.
    """

    appearance: Optional[str] = None
    abilities: Optional[str] = None
    backstory: Optional[str] = None


class UserProfileUpdateResponse(BaseModel):
    """
    This model encapsulates the response sent back to the user after a successful profile update operation. It provides confirmation of the changes applied.
    """

    success: bool
    message: str
    updatedNickname: Optional[str] = None
    updatedAvatarUrl: Optional[str] = None


async def update_user_profile(
    user_id: str,
    nickname: str,
    avatarUrl: Optional[str],
    characterDetails: CharacterConfigUpdate,
) -> UserProfileUpdateResponse:
    """
    Update the user's profile information.

    Args:
    user_id (str): The unique identifier of the user whose profile is being updated. This ensures that the correct profile is targeted for updates.
    nickname (str): The new nickname to be updated in the user's profile. This allows for personalization of the user experience within the game.
    avatarUrl (Optional[str]): The URL of the new avatar image. Reflects the user's preferred avatar, enhancing the customized game experience.
    characterDetails (CharacterConfigUpdate): Structured information for updating the user's character configurations. This includes appearance, abilities, and backstory adjustments.

    Returns:
    UserProfileUpdateResponse: This model encapsulates the response sent back to the user after a successful profile update operation. It provides confirmation of the changes applied.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if user is None:
        return UserProfileUpdateResponse(success=False, message="User not found.")
    await prisma.models.UserProfile.prisma().update(
        where={"userId": user_id}, data={"nickname": nickname, "avatarUrl": avatarUrl}
    )
    if (
        characterDetails.appearance
        or characterDetails.abilities
        or characterDetails.backstory
    ):
        await prisma.models.CharacterConfig.prisma().update_many(
            where={"userProfile": {"userId": user_id}},
            data={
                "appearance": characterDetails.appearance,
                "abilities": characterDetails.abilities,
                "backstory": characterDetails.backstory,
            },
        )
    return UserProfileUpdateResponse(
        success=True,
        message="User profile updated successfully.",
        updatedNickname=nickname,
        updatedAvatarUrl=avatarUrl,
    )
