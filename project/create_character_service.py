from typing import Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateCharacterResponse(BaseModel):
    """
    A response model signaling the successful creation of the character with a summary of the character's main attributes.
    """

    characterId: str
    message: str


async def create_character(
    userId: str,
    appearance: Dict[str, str],
    abilities: Dict[str, int],
    backstory: Optional[str] = None,
) -> CreateCharacterResponse:
    """
    Allows players to create a new character.

    Args:
        userId (str): The unique identifier of the user creating the character.
        appearance (Dict[str, str]): A JSON object detailing the character's appearance options such as hair color, eye shape, etc.
        abilities (Dict[str, int]): A JSON object detailing the character's abilities, including strength, intelligence, dexterity, etc.
        backstory (Optional[str]): An optional text field for players to provide a backstory for their character.

    Returns:
        CreateCharacterResponse: A response model signaling the successful creation of the character with a summary of the character's main attributes.

    Example:
        create_character(
            userId="some-unique-user-id",
            appearance={"hairColor": "red", "eyeShape": "round"},
            abilities={"strength": 10, "intelligence": 8, "dexterity": 6},
            backstory="Born under the mountain..."
        )
        > CreateCharacterResponse(characterId="some-unique-character-id", message="Character successfully created.")
    """
    user_profile = await prisma.models.UserProfile.prisma().find_first(
        where={"userId": userId}
    )
    if not user_profile:
        raise ValueError("UserProfile does not exist for given userId")
    new_character = await prisma.models.CharacterConfig.prisma().create(
        data={
            "profileId": user_profile.id,
            "appearance": appearance,
            "abilities": abilities,
            "backstory": backstory,
        }
    )
    return CreateCharacterResponse(
        characterId=new_character.id, message="Character successfully created."
    )
