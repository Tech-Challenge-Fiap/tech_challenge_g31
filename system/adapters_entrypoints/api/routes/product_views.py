from app import app
from flask import request
from pydantic import ValidationError
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.product_exceptions import ProductAlreadyExistsError, ProductDoesNotExistError, ProductTypeError, ProductUpdateError
from system.application.usecase import products_usecase
from system.application.dto.requests.product_request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from system.infrastructure.adapters.decorators.jwt_decorator import require_auth


@app.route("/create_product", methods=["POST"])
@require_auth
def create_product():
    try:
        create_product_request = CreateProductRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        product = products_usecase.CreateProductUseCase.execute(request=create_product_request)
    except ProductAlreadyExistsError:
        return {"error": "This product already exists"}, 409
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return product.response


@app.route("/get_product/<product_id>", methods=["GET"])
@require_auth
def get_product_by_id(product_id):
    try:
        product = products_usecase.GetProductByIDUseCase.execute(product_id=product_id)
    except ProductDoesNotExistError:
        return {"error": "This Product does not exist"}, 404
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return product.response


@app.route("/get_products/", methods=["GET"])
@require_auth
def get_products():
    try:
        products = products_usecase.GetAllProductsUseCase.execute()
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return products.response


@app.route("/get_products/<product_type>", methods=["GET"])
@require_auth
def get_products_by_type(product_type):
    try:
        products = products_usecase.GetProductsByTypeUseCase.execute(product_type=product_type)
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    except ProductTypeError:
        return {"error": "This Product Type does not exist"}, 400
    return products.response

@app.route("/delete_product/<product_id>", methods=["DELETE"])
@require_auth
def delete_product(product_id):
    try:
        products_usecase.DeleteProductUseCase.execute(product_id=product_id)
    except ProductDoesNotExistError:
        return {"error": "This Product does not exist"}, 404
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return "", 204


@app.route("/update_product/<product_id>", methods=["PATCH"])
@require_auth
def update_product(product_id: int):
    try:
        update_product_request = UpdateProductRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        product = products_usecase.UpdateProductUseCase.execute(
            product_id=product_id, request=update_product_request
        )
    except ProductDoesNotExistError:
        return {"error": "This Product does not exist"}, 404
    except ProductUpdateError:
        return {"error": "This Product could not be updated"}, 400
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return product.response

@app.route("/enable_product/<product_id>", methods=["PATCH"])
@require_auth
def enable_product(product_id):
    try:
        product =products_usecase.EnableProductUseCase.execute(product_id=product_id)
    except ProductDoesNotExistError:
        return {"error": "This Product does not exist"}, 404
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return product.response

@app.route("/get_deleted_products/", methods=["GET"])
@require_auth
def get_deleted_products():
    try:
        products = products_usecase.GetDeletedProductsUseCase.execute()
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return products.response