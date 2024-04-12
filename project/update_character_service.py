from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateCharacterResponse(BaseModel):
    """
    Response model for a successful character update operation. Returns the updated character details.
    """

    success: bool
    message: str
    updated_character: Optional[Dict[str, Any]] = None


async def update_character(
    character_id: str,
    new_appearance: Dict[str, Any],
    new_abilities: Dict[str, Any],
    new_backstory: Optional[str],
) -> UpdateCharacterResponse:
    """
    Updates a character's customization options.

    Args:
    character_id (str): ID of the character to update.
    new_appearance (Dict[str, Any]): A JSON formatted string with new values for character appearance customization.
    new_abilities (Dict[str, Any]): A JSON formatted string detailing the new abilities assigned to the character.
    new_backstory (Optional[str]): Optional. A new or updated backstory for the character.

    Returns:
    UpdateCharacterResponse: Response model for a successful character update operation. Returns the updated character details.
    """
    character = await prisma.models.CharacterConfig.prisma().find_unique(
        where={"id": character_id}
    )
    if character:
        update_data = {"appearance": new_appearance, "abilities": new_abilities}
        if new_backstory is not None:
            update_data["backstory"] = new_backstory
        updated_character = await prisma.models.CharacterConfig.prisma().update(
            where={"id": character_id}, data=update_data
        )
        return UpdateCharacterResponse(
            success=True,
            message="Character updated successfully",
            updated_character={
                "appearance": updated_character.appearance,
                "abilities": updated_character.abilities,
                "backstory": updated_character.backstory,
            },
        )
    else:
        return UpdateCharacterResponse(
            success=False, message="Character not found", updated_character=None
        )
