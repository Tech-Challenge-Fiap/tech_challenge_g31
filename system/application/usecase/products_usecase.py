from flask_restful import Resource
from psycopg2 import IntegrityError
from system.application.dto.requests.product_request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from system.application.dto.responses.product_response import (
    CreateProductResponse,
    GetAllProductsResponse,
    GetProductByIDResponse,
    GetProductsByTypeResponse,
    UpdateProductResponse,
)
from system.domain.entities.product import ProductEntity
from system.infrastructure.adapters.database.exceptions.product_exceptions import (
    ProductAlreadyExistsError,
    ProductDoesNotExistError,
)

from system.infrastructure.adapters.database.repositories.product_repository import (
    ProductRepository,
)


class CreateProductUseCase(Resource):
    def execute(request: CreateProductRequest) -> CreateProductResponse:
        """
        Create product
        """
        product = ProductEntity(**request.model_dump())
        try:
            response = ProductRepository.create_product(product)
        except IntegrityError as err:
            raise ProductAlreadyExistsError(str(err))

        return CreateProductResponse(response.model_dump())


class GetProductByIDUseCase(Resource):
    def execute(product_id: int) -> GetProductByIDResponse:
        """
        Get product by its id
        """
        response = ProductRepository.get_product_by_id(product_id)
        return GetProductByIDResponse(response.model_dump())


class GetAllProductsUseCase(Resource):
    def execute() -> GetAllProductsResponse:
        """
        Get products with filters
        """
        response = ProductRepository.get_all_products()

        return GetAllProductsResponse(response)


class GetProductsByTypeUseCase(Resource):
    def execute(product_type: int) -> GetProductsByTypeResponse:
        """
        Get product by its id
        """
        try:
            response = ProductRepository.get_products_by_type(product_type)
        except IntegrityError as err:
            raise ProductDoesNotExistError(str(err))

        return GetProductsByTypeResponse(response)


class DeleteProductUseCase(Resource):
    def execute(product_id: int) -> None:
        """Delete a product by its id"""
        ProductRepository.delete_product_by_id(product_id)


class UpdateProductUseCase(Resource):
    def execute(
        product_id: int,
        request: UpdateProductRequest,
    ) -> UpdateProductResponse:
        """Update product"""
        product = ProductRepository.update_product(product_id, request)

        return UpdateProductResponse(product.model_dump())
