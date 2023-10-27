from pydantic import BaseModel
from typing import Optional

from system.domain.enums.enums import ProductTypeEnum


class ProductEntity(BaseModel):
    product_id: Optional[int] = None
    type: ProductTypeEnum
    name: str
    price: float
    prep_time: int
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True
