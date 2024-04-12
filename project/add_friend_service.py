import prisma
import prisma.models
from pydantic import BaseModel


class AddFriendResponseModel(BaseModel):
    """
    Provides feedback on the success or failure of the add friend request operation.
    """

    success: bool
    message: str


async def add_friend(sender_id: str, receiver_id: str) -> AddFriendResponseModel:
    """
    Allows players to add other players as friends.

    Args:
    sender_id (str): The user ID of the player sending the friend request.
    receiver_id (str): The user ID of the player who is intended to receive the friend request.

    Returns:
    AddFriendResponseModel: Provides feedback on the success or failure of the add friend request operation.
    """
    if sender_id == receiver_id:
        return AddFriendResponseModel(
            success=False, message="Cannot send a friend request to yourself."
        )
    existing_users = await prisma.models.User.prisma().find_many(
        where={"id": {"in": [sender_id, receiver_id]}}
    )
    if len(existing_users) < 2:
        return AddFriendResponseModel(
            success=False, message="Either sender or receiver does not exist."
        )
    existing_request = await prisma.models.FriendRequest.prisma().find_first(
        where={
            "OR": [
                {"senderId": sender_id, "receiverId": receiver_id},
                {"senderId": receiver_id, "receiverId": sender_id},
            ]
        }
    )
    if existing_request:
        return AddFriendResponseModel(
            success=False,
            message="A friend request already exists between these users.",
        )
    await prisma.models.FriendRequest.prisma().create(
        data={"senderId": sender_id, "receiverId": receiver_id, "status": "PENDING"}
    )
    return AddFriendResponseModel(
        success=True, message="Friend request sent successfully."
    )
