from typing import List, Optional
from pydantic import BaseModel

from system.domain.enums.enums import OrderStatusEnum


class CreateOrderRequest(BaseModel):
    products: List[int]
    client_id: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatusEnum

    class Config:
        from_attributes = True
