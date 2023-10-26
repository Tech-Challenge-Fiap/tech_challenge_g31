from pydantic import BaseModel
from typing import Optional


class ProductEntity(BaseModel):
    product_id: Optional[int] = None
    type: str
    name: str
    price: float
    prep_time: int
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True
