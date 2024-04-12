from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class FriendDetail(BaseModel):
    """
    Details about a friend including their user ID, nickname, and other relevant information.
    """

    friend_id: str
    nickname: str
    avatar_url: Optional[str] = None


class GetFriendsListResponse(BaseModel):
    """
    Provides a list of friends for the requesting user, including relevant details for each friend.
    """

    friends: List[FriendDetail]


async def get_friends_list(user_id: str) -> GetFriendsListResponse:
    """
    Retrieves the player's list of friends based on established friendships in the database.

    Args:
        user_id (str): The unique identifier of the user requesting their friends list.

    Returns:
        GetFriendsListResponse: Provides a list of friends for the requesting user, including relevant details for each friend.
    """
    friendships = await prisma.models.Friendship.prisma().find_many(
        where={"userId": user_id}, include={"friend": {"include": {"profiles": True}}}
    )
    friends_details = []
    for friendship in friendships:
        for profile in friendship.friend.profiles:
            friend_detail = FriendDetail(
                friend_id=friendship.friendId,
                nickname=profile.nickname,
                avatar_url=profile.avatarUrl,
            )
            friends_details.append(friend_detail)
    return GetFriendsListResponse(friends=friends_details)
