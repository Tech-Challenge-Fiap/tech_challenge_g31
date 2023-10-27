from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from system.domain.entities.payment import PaymentEntity
from system.domain.entities.product import ProductEntity
from system.domain.enums.enums import OrderStatusEnum


class OrderEntity(BaseModel):
    order_id: Optional[int] = None
    order_date: datetime = datetime.today().date()
    price: Optional[Decimal] = None
    products_ids: List[int]
    status: str = OrderStatusEnum.RECIEVED.value
    waiting_time: Optional[int] = None
    client_id: Optional[str] = None
    payment: PaymentEntity

    class Config:
        from_attributes = True
