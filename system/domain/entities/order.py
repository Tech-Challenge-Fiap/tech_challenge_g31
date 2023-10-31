from decimal import Decimal
from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional
from system.domain.entities.payment import PaymentEntity
from system.domain.entities.product import BasicProductEntity
from system.domain.enums.enums import OrderStatusEnum


class OrderEntity(BaseModel):
    order_id: Optional[int] = None
    order_date: datetime = datetime.today().date()
    price: Optional[Decimal] = None
    products_ids: Optional[List[int]] = None
    products: Optional[List[BasicProductEntity]] = None
    status: OrderStatusEnum = OrderStatusEnum.TO_BE_PAYED
    waiting_time: Optional[int] = None
    client_id: Optional[str] = None
    payment: PaymentEntity

    class Config:
        from_attributes = True
        use_enum_values = True

    @validator("products", pre=True, always=True)
    def validate_exclusive_fields(cls, value, values):
        products_ids = values.get("products_ids")
        if value is None and products_ids is None:
            raise ValueError("Deve ser fornecido products_ids ou products")
        return value
