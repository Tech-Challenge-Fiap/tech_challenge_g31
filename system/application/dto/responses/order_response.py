from datetime import datetime
from typing import List, Optional
from flask import Response



class OrderResponse(Response):
    order_id: int
    order_date: datetime
    products: List[int]
    status: str
    waiting_time: int
    client_id: Optional[str]
    payment_id: int

    class Config:
        from_attributes = True


class CreateOrderResponse(OrderResponse):
    pass


class GetOrderByIDResponse(OrderResponse):
    pass


class GetAllOrdersResponse(OrderResponse):
    orders: List[OrderResponse]


class UpdateOrderResponse(OrderResponse):
    pass
