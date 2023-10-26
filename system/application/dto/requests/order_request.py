from typing import List, Optional
from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    products: List[int]
    client_cpf: Optional[str]

    class Config:
        from_attributes = True


class UpdateOrderStatusRequest(BaseModel):
    status: str

    class Config:
        from_attributes = True
