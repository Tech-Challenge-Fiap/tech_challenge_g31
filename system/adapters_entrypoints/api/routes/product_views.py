from app import app
from flask import request
from pydantic import ValidationError
from system.application.usecase import products_usecase
from system.application.dto.requests.product_request import (
    CreateProductRequest,
    UpdateProductRequest,
)
from system.infrastructure.adapters.database.exceptions.product_exceptions import (
    ProductDeleteError,
    ProductDoesNotExistError,
    ProductUpdateError,
)


@app.route("/create_product", methods=["POST"])
def create_product():
    try:
        create_product_request = CreateProductRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        product = products_usecase.CreateProductUseCase.execute(request=create_product_request)
    except Exception:
        return {"error": "Internal Error"}, 500
    product.response["type"] = product.response["type"].value
    return product.response


@app.route("/get_product/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product = products_usecase.GetProductByIDUseCase.execute(product_id=product_id)
    except ProductDoesNotExistError:
        return {"error": "This Product does not exist"}, 404
    except Exception:
        return {"error": "Internal Error"}, 500
    return product.response


@app.route("/get_products/", methods=["GET"])
def get_products():
    try:
        products = products_usecase.GetAllProductsUseCase.execute()
    except Exception:
        return {"error": "Internal Error"}, 500
    products_list = []
    for product in products.response:
        products_list.append(vars(product))
    return products_list


@app.route("/get_products/<product_type>", methods=["GET"])
def get_products_by_type(product_type):
    try:
        products = products_usecase.GetProductsByTypeUseCase.execute(product_type=product_type)
    except Exception:
        return {"error": "Internal Error"}, 500
    products_list = []
    for product in products.response:
        products_list.append(vars(product))
    return products_list

@app.route("/delete_product/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        products_usecase.DeleteProductUseCase.execute(product_id=product_id)
    except ProductDoesNotExistError:
        return {"error": "This Product does not exist"}, 404
    except ProductDeleteError:
        return {"error": "This Product can not be deleted"}, 400
    except Exception:
        return {"error": "Internal Error"}, 500
    return "", 204


@app.route("/update_product/<product_id>", methods=["PATCH"])
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
        return {"error": "This Product can not be updated"}, 400
    except Exception as ex:
        return {"error": "Internal Error"}, 500
    return product.response, 200
