from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from system.domain.enums.enums import OrderStatusEnum


class OrderEntity(BaseModel):
    order_id: Optional[int] = None
    order_date: datetime  = datetime.today().date()
    products: List[int]
    status: OrderStatusEnum = OrderStatusEnum.RECIEVED
    waiting_time: Optional[int] = None
    client_id: Optional[str] = None
    payment_id: Optional[int] = None

    class Config:
        from_attributes = True
    