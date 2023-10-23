from typing import Optional
from pydantic import BaseModel

from system.domain.enums.enums import ProductTypeEnum

class ProductPayload(BaseModel):
    type: ProductTypeEnum
    name: str
    price: float
    prep_time: int
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True

class CreateProductRequest(ProductPayload):
    pass

class UpdateProductRequest(BaseModel):
    type: Optional[ProductTypeEnum] = None
    name: Optional[str] = None
    price: Optional[float] = None
    prep_time: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True