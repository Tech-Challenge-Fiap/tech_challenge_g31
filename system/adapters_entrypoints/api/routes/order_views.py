from app import app
from flask import request
from pydantic import ValidationError
from system.application.dto.requests.payment_request import PaymentRequest
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.order_exceptions import (
    OrderDoesNotExistError,
    OrderUpdateError,
)
from system.application.exceptions.product_exceptions import ProductDoesNotExistError
from system.application.usecase import order_usecase, payment_usecase
from system.application.dto.requests.order_request import (
    CreateOrderRequest,
    UpdateOrderStatusRequest,
)
from system.infrastructure.adapters.database.repositories.order_repository import OrderRepository
from system.infrastructure.adapters.database.repositories.payment_repository import PaymentRepository
from system.infrastructure.adapters.database.repositories.product_repository import ProductRepository
from system.infrastructure.adapters.external_tools.mercado_pago import MercadoPago


@app.route("/update_status/<order_id>", methods=["PATCH"])
def checkout_order(order_id):
    try:
        mercado_pago_request = PaymentRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        order = order_usecase.CheckoutOrderUseCase.execute(
            order_id=order_id,
            request=mercado_pago_request,
            order_repository=OrderRepository,
            payment_repository=PaymentRepository
        )
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    except OrderDoesNotExistError:
        return {"error": "This Order does not exist"}, 404
    return order.response


@app.route("/create_order", methods=["POST"])
def create_order():
    try:
        create_order_request = CreateOrderRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        order = order_usecase.CreateOrderUseCase.execute(
            request=create_order_request,
            order_repository=OrderRepository,
            product_repository=ProductRepository,
            payment_repository=PaymentRepository,
            payment_service=MercadoPago
        )
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    except OrderDoesNotExistError:
        return {"error": "This Order does not exist"}, 404
    except ProductDoesNotExistError:
        return {"error": "Product does not exist"}, 400
    return order.response


@app.route("/get_order/<order_id>", methods=["GET"])
def get_order_by_id(order_id):
    try:
        order = order_usecase.GetOrderByIDUseCase.execute(order_id=order_id, order_repository=OrderRepository,)
    except OrderDoesNotExistError:
        return {"error": "This Order does not exist"}, 404
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return order.response


@app.route("/get_orders/", methods=["GET"])
def get_orders():
    try:
        orders = order_usecase.GetAllOrdersUseCase.execute(order_repository=OrderRepository,)
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return orders.response


@app.route("/patch_order/<order_id>", methods=["PATCH"])
def patch_order(order_id):
    try:
        update_order_request = UpdateOrderStatusRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        order = order_usecase.UpdateOrderStatusUseCase.execute(
            order_id=order_id, status=update_order_request.status, order_repository=OrderRepository,
        )
    except OrderDoesNotExistError:
        return "This Order does not exist", 400
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    except OrderUpdateError:
        return {"error": "This Order could not be updated"}, 400
    return order.response


@app.route("/get_order/payment/<order_id>", methods=["GET"])
def check_order_payment(order_id):
    try:
        order = payment_usecase.UpdateOrderPaymentUseCase.execute(order_id=order_id, order_repository=OrderRepository)
    except OrderDoesNotExistError:
        return "This Order does not exist", 400
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return order.response

@app.route("/get_active_orders/", methods=["GET"])
def get_active_orders():
    try:
        orders = order_usecase.GetOrdersUseCase.execute(order_repository=OrderRepository,)
    except InfrastructureError:
        return {"error": "Internal Error"}, 500
    return orders.response