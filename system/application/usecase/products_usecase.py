from flask_restful import Resource
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
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.product_exceptions import ProductDoesNotExistError, ProductTypeError
from system.application.usecase.usecases import UseCase, UseCaseNoRequest
from system.domain.entities.product import ProductEntity
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import InvalidInputError, NoObjectFoundError, PostgreSQLError
from system.infrastructure.adapters.database.repositories.product_repository import ProductRepository


class CreateProductUseCase(UseCase, Resource):
    def execute(request: CreateProductRequest) -> CreateProductResponse:
        """
        Create product
        """
        product = ProductEntity(**request.model_dump())
        try:
            response = ProductRepository.create_product(product)
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))

        return CreateProductResponse(response.model_dump())


class GetProductByIDUseCase(UseCase, Resource):
    def execute(product_id: int) -> GetProductByIDResponse:
        """
        Get product by its id
        """
        try:
            response = ProductRepository.get_product_by_id(product_id)
        except NoObjectFoundError:
            raise ProductDoesNotExistError
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        return GetProductByIDResponse(response.model_dump())


class GetAllProductsUseCase(UseCaseNoRequest, Resource):
    def execute() -> GetAllProductsResponse:
        """
        Get products with filters
        """
        try:
            response = ProductRepository.get_all_products()
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        return GetAllProductsResponse(response)


class GetProductsByTypeUseCase(UseCase, Resource):
    def execute(product_type: int) -> GetProductsByTypeResponse:
        """
        Get product by its id
        """
        try:
            response = ProductRepository.get_products_by_type(product_type)
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        except InvalidInputError:
            raise ProductTypeError
        return GetProductsByTypeResponse(response)


class DeleteProductUseCase(UseCase, Resource):
    def execute(product_id: int) -> None:
        """Delete a product by its id"""
        try:
            ProductRepository.delete_product_by_id(product_id)
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        except NoObjectFoundError:
            raise ProductDoesNotExistError

class UpdateProductUseCase(UseCase, Resource):
    def execute(
        product_id: int,
        request: UpdateProductRequest,
    ) -> UpdateProductResponse:
        """Update product"""
        try:
            product = ProductRepository.update_product(product_id, request)
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        except NoObjectFoundError:
            raise ProductDoesNotExistError
        return UpdateProductResponse(product.model_dump())
