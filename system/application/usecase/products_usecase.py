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
from system.application.exceptions.repository_exceptions import DataRepositoryExeption, InvalidInputError, NoObjectFoundError
from system.application.ports.product_port import ProductPort
from system.application.usecase.usecases import UseCase, UseCaseNoRequest
from system.domain.entities.product import ProductEntity


class CreateProductUseCase(UseCase, Resource):
    def execute(request: CreateProductRequest, product_repository: ProductPort) -> CreateProductResponse:
        """
        Create product
        """
        product = ProductEntity(**request.model_dump())
        try:
            response = product_repository.create_product(product)
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))

        return CreateProductResponse(response.model_dump())


class GetProductByIDUseCase(UseCase, Resource):
    def execute(product_id: int, product_repository: ProductPort) -> GetProductByIDResponse:
        """
        Get product by its id
        """
        try:
            response = product_repository.get_product_by_id(product_id)
        except NoObjectFoundError:
            raise ProductDoesNotExistError
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return GetProductByIDResponse(response.model_dump())


class GetAllProductsUseCase(UseCaseNoRequest, Resource):
    def execute(product_repository: ProductPort) -> GetAllProductsResponse:
        """
        Get products with filters
        """
        try:
            response = product_repository.get_all_products()
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        response = [r.model_dump() for r in response]
        return GetAllProductsResponse(response)


class GetProductsByTypeUseCase(UseCase, Resource):
    def execute(product_type: int, product_repository: ProductPort) -> GetProductsByTypeResponse:
        """
        Get product by its id
        """
        try:
            response = product_repository.get_products_by_type(product_type)
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        except InvalidInputError:
            raise ProductTypeError
        response = [r.model_dump() for r in response]
        return GetProductsByTypeResponse(response)


class DeleteProductUseCase(UseCase, Resource):
    def execute(product_id: int, product_repository: ProductPort) -> None:
        """Delete a product by its id"""
        try:
            product_repository.delete_product_by_id(product_id)
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        except NoObjectFoundError:
            raise ProductDoesNotExistError

class UpdateProductUseCase(UseCase, Resource):
    def execute(
        product_id: int,
        request: UpdateProductRequest,
        product_repository: ProductPort
    ) -> UpdateProductResponse:
        """Update product"""
        try:
            product = product_repository.update_product(product_id, request)
        except NoObjectFoundError:
            raise ProductDoesNotExistError
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        return UpdateProductResponse(product.model_dump())

class EnableProductUseCase(UseCase, Resource):
    def execute(product_id: int, product_repository: ProductPort) -> None:
        """Enable a product by its id"""
        try:
            product = product_repository.enable_product_by_id(product_id)
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        except NoObjectFoundError:
            raise ProductDoesNotExistError
        return UpdateProductResponse(product.model_dump())

class GetDeletedProductsUseCase(UseCaseNoRequest, Resource):
    def execute(product_repository: ProductPort) -> GetAllProductsResponse:
        """
        Get products with filters
        """
        try:
            response = product_repository.get_deleted_products()
        except DataRepositoryExeption as err:
            raise InfrastructureError(str(err))
        response = [r.model_dump() for r in response]
        return GetAllProductsResponse(response)