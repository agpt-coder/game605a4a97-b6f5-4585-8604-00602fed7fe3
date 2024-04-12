from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class PaymentMethod(BaseModel):
    """
    A detailed structure capturing the payment method information.
    """

    type: str
    details: str


class PurchaseItemResponse(BaseModel):
    """
    Response model for in-game item purchase requests, capturing the result of the transaction.
    """

    transaction_id: str
    status: str
    message: Optional[str] = None


async def purchase_item(
    user_id: str, item_id: str, quantity: int, payment_method: PaymentMethod
) -> PurchaseItemResponse:
    """
    Process in-game item purchases.

    Args:
    user_id (str): The unique identifier for the user making the purchase.
    item_id (str): The unique identifier of the item being purchased.
    quantity (int): The quantity of the item being purchased.
    payment_method (PaymentMethod): Details of the payment method used for the purchase.

    Returns:
    PurchaseItemResponse: Response model for in-game item purchase requests, capturing the result of the transaction.
    """
    item = await prisma.models.Item.prisma().find_unique(where={"id": item_id})
    if not item:
        return PurchaseItemResponse(
            transaction_id="", status="failed", message="prisma.models.Item not found"
        )
    total_cost = item.price * quantity
    payment_success = True
    if payment_success:
        purchase_record = await prisma.models.Purchase.prisma().create(
            data={"userId": user_id, "itemId": item_id, "amount": total_cost}
        )
        return PurchaseItemResponse(
            transaction_id=purchase_record.id,
            status="success",
            message="prisma.models.Purchase successful",
        )
    else:
        return PurchaseItemResponse(
            transaction_id="", status="failed", message="Payment failed"
        )
