from typing import List, Optional
from flask import Response

from system.domain.enums.enums import ProductTypeEnum



class ProductResponse(Response):
    product_id: int
    type: ProductTypeEnum
    name: str
    price: float
    prep_time: int
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True


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
