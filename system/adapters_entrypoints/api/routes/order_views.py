from app import app
from flask import request
from psycopg2 import IntegrityError
from system.application.dto.requests.order_request import CreateOrderRequest, UpdateOrderStatusRequest
from system.application.usecase.order_usecase import CreateOrderUseCase, GetAllOrdersUseCase, GetOrderByIDUseCase, UpdateOrderStatusUseCase
from system.infrastructure.adapters.database.exceptions.order_exceptions import OrderAlreadyExistsError, OrderDoesNotExistError


@app.route('/create_order', methods=['POST'])
def create_order():
    create_order_request = CreateOrderRequest(**request.get_json())
    try:
        order = CreateOrderUseCase.execute(request=create_order_request)
    except OrderAlreadyExistsError:
            return "This Order already exists", 400
    order.response['type'] = str(order.response['type']).split(".")[1]
    return order.response

@app.route('/get_order/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    try:
        order = GetOrderByIDUseCase.execute(order_id=order_id)
    except OrderDoesNotExistError as err:
            return "This Order does not exist", 400
    order.response['type'] = str(order.response['type']).split(".")[1]
    return order.response

@app.route('/get_orders/', methods=['GET'])
def get_orders():
    try:
        orders = GetAllOrdersUseCase.execute()
    except IntegrityError:
            return "Internal Error", 500
    orders_list = []
    for order in orders.response:
        a=1 #Não sei pq não funciona sem uma linha antes do split abaixo
        order.type = str(order.type).split(".")[1]
        orders_list.append(vars(order))
    return orders_list

@app.route('/patch_order/<order_id>', methods=['PATCH'])
def patch_order(order_id):
    update_order_request = UpdateOrderStatusRequest(**request.get_json())
    try:
        order = UpdateOrderStatusUseCase.execute(order_id=order_id, status=update_order_request.status)
    except OrderDoesNotExistError:
        return "This Order does not exist", 400
    
    order.response['type'] = str(order.response['type']).split(".")[1]
    return order.response
