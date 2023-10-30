from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from system.domain.entities.payment import PaymentEntity
from system.domain.enums.enums import OrderStatusEnum, ProductTypeEnum


class OrderProductEntity(BaseModel):
    product_id: int
    quantity: Optional[int] = None
    type: Optional[ProductTypeEnum] = None
    name: Optional[str] = None
    price: Optional[float] = None
    prep_time: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class OrderEntity(BaseModel):
    order_id: Optional[int] = None
    order_date: datetime = datetime.today().date()
    price: Optional[Decimal] = None
    status: OrderStatusEnum = OrderStatusEnum.TO_BE_PAYED
    waiting_time: Optional[int] = None
    client_id: Optional[str] = None
    payment: PaymentEntity
    products: List[OrderProductEntity]

    class Config:
        from_attributes = True
        use_enum_values = True
