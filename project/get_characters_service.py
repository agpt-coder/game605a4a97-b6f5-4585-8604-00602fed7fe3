from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CharacterSummary(BaseModel):
    """
    Summarizes the essential details of a character for listing purposes.
    """

    id: str
    nickname: str
    appearance: str
    abilities: str
    backstory: Optional[str] = None


class GetCharactersResponse(BaseModel):
    """
    Provides a summarized list of all characters associated with the user, including basic details for display.
    """

    characters: List[CharacterSummary]


async def get_characters() -> GetCharactersResponse:
    """
    Retrieves a list of the user's characters.

    Args:

    Returns:
    GetCharactersResponse: Provides a summarized list of all characters associated with the user, including basic details for display.
    """
    characters = await prisma.models.CharacterConfig.prisma().find_many(
        include={"userProfile": {"include": {"user": True}}}
    )
    character_summaries = [
        CharacterSummary(
            id=character.id,
            nickname=character.userProfile.nickname,
            appearance=str(character.appearance),
            abilities=str(character.abilities),
            backstory=character.backstory,
        )
        for character in characters
    ]
    return GetCharactersResponse(characters=character_summaries)
