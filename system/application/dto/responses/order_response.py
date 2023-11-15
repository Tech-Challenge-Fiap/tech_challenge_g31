from datetime import datetime
from typing import List, Optional
from flask import Response
from system.domain.entities.product import BasicProductEntity

from system.domain.enums.enums import OrderStatusEnum, PaymentStatusEnum


class OrderResponse(Response):
    order_id: int
    order_date: datetime
    products: List[BasicProductEntity]
    status: OrderStatusEnum
    waiting_time: int
    client_id: Optional[str]
    payment_id: int

    class Config:
        from_attributes = True
        use_enum_values = True


class CreateOrderResponse(OrderResponse):
    pass


class GetOrderByIDResponse(OrderResponse):
    pass


class GetAllOrdersResponse(OrderResponse):
    orders: List[OrderResponse]


class UpdateOrderResponse(OrderResponse):
    pass


class CheckOrderPaymentResponse(Response):
    id: int
    payment_status: PaymentStatusEnum
    qr_code: str
    status_updated_at: Optional[datetime]
    status: str

    class Config:
        from_attributes = True
        use_enum_values = True
