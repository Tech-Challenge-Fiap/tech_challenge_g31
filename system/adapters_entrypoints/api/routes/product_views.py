from app import app
from flask import request
from psycopg2 import IntegrityError
from system.application.dto.requests.product_request import CreateProductRequest, UpdateProductRequest
from system.application.usecase.products_usecase import CreateProductUseCase, DeleteProductUseCase, GetAllProductsUseCase, GetProductByIDUseCase, GetProductsByTypeUseCase, UpdateProductUseCase
from system.infrastructure.adapters.database.exceptions.product_exceptions import ProductAlreadyExistsError, ProductDoesNotExistError  # Importe o Flask-Migrate


@app.route('/create_product', methods=['POST'])
def create_product():
    create_product_request = CreateProductRequest(**request.get_json())
    try:
        product = CreateProductUseCase.execute(request=create_product_request)
    except ProductAlreadyExistsError:
            return "This Product already exists", 400
    product.response['type'] = str(product.response['type']).split(".")[1]
    return product.response

@app.route('/get_product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        product = GetProductByIDUseCase.execute(product_id=product_id)
    except ProductDoesNotExistError as err:
            return "This Product does not exist", 400
    product.response['type'] = str(product.response['type']).split(".")[1]
    return product.response

@app.route('/get_products/', methods=['GET'])
def get_products():
    try:
        products = GetAllProductsUseCase.execute()
    except IntegrityError:
            return "Internal Error", 500
    products_list = []
    for product in products.response:
        a=1 #Não sei pq não funciona sem uma linha antes do split abaixo
        product.type = str(product.type).split(".")[1]
        products_list.append(vars(product))
    return products_list

@app.route('/get_products/<product_type>', methods=['GET'])
def get_products_by_type(product_type):
    try:
        products = GetProductsByTypeUseCase.execute(product_type=product_type)
    except IntegrityError:
            return "Internal Error", 500
    products_list = []
    for product in products.response:
        a=1 #Não sei pq não funciona sem uma linha antes do split abaixo
        product.type = str(product.type).split(".")[1]
        products_list.append(vars(product))
    return products_list

@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        DeleteProductUseCase.execute(product_id=product_id)
    except ProductDoesNotExistError as err:
            return "This Product does not exist", 400
    return "", 204

@app.route('/update_product/<product_id>', methods=['PATCH'])
def update_product(product_id):
    update_product_request = UpdateProductRequest(**request.get_json())
    try:
        product = UpdateProductUseCase.execute(product_id=product_id, request=update_product_request)
    except ProductDoesNotExistError:
            return "This Product does not exists", 400
    product.response.type = str(product.response.type).split(".")[1]
    return product.response.__dict__