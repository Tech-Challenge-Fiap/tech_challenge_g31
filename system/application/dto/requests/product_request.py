from typing import Optional
from pydantic import BaseModel



class ProductPayload(BaseModel):
    type: str
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
    name: Optional[str] = None
    price: Optional[float] = None
    prep_time: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True
