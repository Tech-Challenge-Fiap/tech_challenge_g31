from app import app
from flask import request
from pydantic import ValidationError
from system.application.usecase import order_usecase
from system.application.dto.requests.order_request import (
    CreateOrderRequest,
    UpdateOrderStatusRequest,
)
from system.infrastructure.adapters.database.exceptions.order_exceptions import (
    OrderDoesNotExistError,
)


@app.route("/checkout", methods=["POST"])
def checkout():
    try:
        create_order_request = CreateOrderRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        order = order_usecase.CheckoutUseCase.execute(request=create_order_request)
    except Exception:
        return {"error": "Internal Error"}, 500
    order.response["status"] = order.response["status"].value
    order.response["payment"]["status"] = order.response["payment"]["status"].value
    return order.response


@app.route("/get_order/<order_id>", methods=["GET"])
def get_order_by_id(order_id):
    try:
        order = order_usecase.GetOrderByIDUseCase.execute(order_id=order_id)
    except OrderDoesNotExistError:
        return {"error": "This Order does not exist"}, 404
    except Exception:
        return {"error": "Internal Error"}, 500
    order.response["status"] = order.response["status"].value
    order.response["payment"]["status"] = order.response["payment"]["status"].value
    return order.response


@app.route("/get_orders/", methods=["GET"])
def get_orders():
    try:
        orders = order_usecase.GetAllOrdersUseCase.execute()
    except Exception:
        return {"error": "Internal Error"}, 500
    for order in orders.response:
        order["status"] = order["status"].value
        order["payment"]["status"] = order["payment"]["status"].value
    return orders.response


@app.route("/patch_order/<order_id>", methods=["PATCH"])
def patch_order(order_id):
    try:
        update_order_request = UpdateOrderStatusRequest(**request.get_json())
    except ValidationError as ex:
        return ex.errors(), 400
    try:
        order = order_usecase.UpdateOrderStatusUseCase.execute(
            order_id=order_id, status=update_order_request.status
        )
    except OrderDoesNotExistError:
        return "This Order does not exist", 400
    except Exception:
        return {"error": "Internal Error"}, 500
    order.response["status"] = order.response["status"].value
    order.response["payment"]["status"] = order.response["payment"]["status"].value
    return order.response
