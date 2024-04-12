from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ItemDetail(BaseModel):
    """
    Detailed information about a specific item available for purchase.
    """

    id: str
    name: str
    description: str
    price: float
    category: prisma.enums.ItemCategory


class GetItemCatalogResponse(BaseModel):
    """
    Defines the structure for the catalog of items available for purchase.
    """

    items: List[ItemDetail]


async def get_item_catalog() -> GetItemCatalogResponse:
    """
    Retrieve the list of items available for purchase.

    This function queries the database for items available and structures the response to conform
    to the GetItemCatalogResponse model which lists all items including their details.

    Args:
        None

    Returns:
        GetItemCatalogResponse: A response model containing a list of items available for purchase.
    """
    items_query_results = await prisma.models.Item.prisma().find_many()
    item_details = [
        ItemDetail(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            category=item.category,
        )
        for item in items_query_results
    ]
    return GetItemCatalogResponse(items=item_details)
