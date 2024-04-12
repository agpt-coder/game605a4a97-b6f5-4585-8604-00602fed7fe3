import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import project.add_friend_service
import project.create_character_service
import project.get_characters_service
import project.get_friends_list_service
import project.get_item_catalog_service
import project.get_user_profile_service
import project.purchase_item_service
import project.register_user_service
import project.update_character_service
import project.update_user_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="game",
    lifespan=lifespan,
    description="Based on the information gathered through our interactions, the vision for the game is detailed as follows: The game is conceptualized as a strategy genre experience, appealing greatly to those interested in critical thinking, planning, and overcoming challenges. Set within a rich medieval fantasy world, this setting allows for immersion in a realm of knights, dragons, and epic quests, providing an escape into a world filled with magic, lore, and historical aesthetics. The gameplay mechanics are envisioned to include both custom character creation and in-game purchases, enhancing player engagement through personalization and offering additional content for an enriched gaming experience. From a technical standpoint, the game will leverage a tech stack consisting of Python and FastAPI for efficient and fast backend services, PostgreSQL for reliable data storage and complex queries, and Prisma ORM for streamlined database operations, all prioritizing performance, security, and scalable architecture. Targeting a broad audience, the game aims to connect players of varying ages, fostering shared experiences among friends and family across generations via engaging gameplay that transcends typical generational divides. Focused on the mobile platform, the game capitalizes on accessibility and innovative gameplay mechanics specific to touch interfaces and mobile devices' portability. This comprehensive project embodies a strategic and immersive gaming experience that reaches a wide audience through its captivating medieval fantasy theme, innovative gameplay, and accessible mobile platform.",
)


@app.put(
    "/user/profile/update",
    response_model=project.update_user_profile_service.UserProfileUpdateResponse,
)
async def api_put_update_user_profile(
    user_id: str,
    nickname: str,
    avatarUrl: Optional[str],
    characterDetails: project.update_user_profile_service.CharacterConfigUpdate,
) -> project.update_user_profile_service.UserProfileUpdateResponse | Response:
    """
    Update the user's profile information.
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            user_id, nickname, avatarUrl, characterDetails
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/register", response_model=project.register_user_service.RegisterUserResponse
)
async def api_post_register_user(
    email: str, password: str
) -> project.register_user_service.RegisterUserResponse | Response:
    """
    Register a new user account.
    """
    try:
        res = await project.register_user_service.register_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/item/purchase", response_model=project.purchase_item_service.PurchaseItemResponse
)
async def api_post_purchase_item(
    user_id: str,
    item_id: str,
    quantity: int,
    payment_method: project.purchase_item_service.PaymentMethod,
) -> project.purchase_item_service.PurchaseItemResponse | Response:
    """
    Process in-game item purchases.
    """
    try:
        res = await project.purchase_item_service.purchase_item(
            user_id, item_id, quantity, payment_method
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/character/list",
    response_model=project.get_characters_service.GetCharactersResponse,
)
async def api_get_get_characters() -> project.get_characters_service.GetCharactersResponse | Response:
    """
    Retrieves a list of the user's characters.
    """
    try:
        res = await project.get_characters_service.get_characters()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/character/update",
    response_model=project.update_character_service.UpdateCharacterResponse,
)
async def api_put_update_character(
    character_id: str,
    new_appearance: Dict[str, Any],
    new_abilities: Dict[str, Any],
    new_backstory: Optional[str],
) -> project.update_character_service.UpdateCharacterResponse | Response:
    """
    Updates a character's customization options.
    """
    try:
        res = await project.update_character_service.update_character(
            character_id, new_appearance, new_abilities, new_backstory
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/social/add_friend",
    response_model=project.add_friend_service.AddFriendResponseModel,
)
async def api_post_add_friend(
    sender_id: str, receiver_id: str
) -> project.add_friend_service.AddFriendResponseModel | Response:
    """
    Allows players to add other players as friends.
    """
    try:
        res = await project.add_friend_service.add_friend(sender_id, receiver_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/social/friends_list",
    response_model=project.get_friends_list_service.GetFriendsListResponse,
)
async def api_get_get_friends_list(
    user_id: str,
) -> project.get_friends_list_service.GetFriendsListResponse | Response:
    """
    Retrieves the player's list of friends.
    """
    try:
        res = await project.get_friends_list_service.get_friends_list(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/character/create",
    response_model=project.create_character_service.CreateCharacterResponse,
)
async def api_post_create_character(
    userId: str,
    appearance: Dict[str, str],
    abilities: Dict[str, int],
    backstory: Optional[str],
) -> project.create_character_service.CreateCharacterResponse | Response:
    """
    Allows players to create a new character.
    """
    try:
        res = await project.create_character_service.create_character(
            userId, appearance, abilities, backstory
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/profile", response_model=project.get_user_profile_service.UserProfileResponse
)
async def api_get_get_user_profile() -> project.get_user_profile_service.UserProfileResponse | Response:
    """
    Retrieve the user's profile information.
    """
    try:
        res = await project.get_user_profile_service.get_user_profile()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/item/catalog",
    response_model=project.get_item_catalog_service.GetItemCatalogResponse,
)
async def api_get_get_item_catalog() -> project.get_item_catalog_service.GetItemCatalogResponse | Response:
    """
    Retrieve the list of items available for purchase.
    """
    try:
        res = await project.get_item_catalog_service.get_item_catalog()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
