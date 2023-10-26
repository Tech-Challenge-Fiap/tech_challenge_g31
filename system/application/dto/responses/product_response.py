from typing import List, Optional
from flask import Response



class ProductResponse(Response):
    product_id: int
    type: str
    name: str
    price: float
    prep_time: int
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True


class CreateProductResponse(ProductResponse):
    pass


class GetProductByIDResponse(ProductResponse):
    pass


class GetAllProductsResponse(ProductResponse):
    products: List[ProductResponse]


class GetProductsByTypeResponse(ProductResponse):
    products: List[ProductResponse]


class UpdateProductResponse(ProductResponse):
    pass
