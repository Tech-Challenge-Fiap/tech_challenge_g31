from flask_restful import Resource
from psycopg2 import IntegrityError
from system.application.dto.requests.order_request import CreateOrderRequest
from system.application.dto.responses.order_response import (
    CreateOrderResponse,
    GetAllOrdersResponse,
    GetOrderByIDResponse,
    UpdateOrderResponse,
)
from system.application.usecase.usecases import UseCase, UseCaseNoRequest
from system.domain.entities.order import OrderEntity
from system.domain.entities.payment import PaymentEntity
from system.infrastructure.adapters.database.exceptions.order_exceptions import (
    OrderAlreadyExistsError,
    OrderUpdateError,
)

from system.infrastructure.adapters.database.repositories.order_repository import (
    OrderRepository,
)
from system.infrastructure.adapters.database.repositories.payment_repository import (
    PaymentRepository,
)
from system.infrastructure.adapters.database.repositories.product_repository import (
    ProductRepository,
)


class CreateOrderUseCase(UseCase, Resource):
    def execute(request: CreateOrderRequest) -> CreateOrderResponse:
        """
        Create order
        """
        order = OrderEntity(**request.model_dump())
        response = OrderRepository.create_order(order)

        return CreateOrderResponse(response.model_dump())


class CheckoutUseCase(UseCase, Resource):
    def execute(request: CreateOrderRequest) -> CreateOrderResponse:
        """
        Checkout
        """
        products = ProductRepository.get_products_by_ids(request.products)
        order_price = 0
        order_waiting_time = 0
        for p in products:
            order_price += p.price
            order_waiting_time += p.prep_time
        qr_code = "qrcode_url"  # mercado_pago.create_qr_code_payment()
        payment = PaymentEntity(qr_code=qr_code)
        order = OrderEntity(
            price=order_price,
            products_ids=request.products,
            waiting_time=order_waiting_time,
            client_id=request.client_cpf,
            payment=payment,
        )
        try:
            order.payment = PaymentRepository.create_payment(payment)
            response = OrderRepository.create_order(order)
        except IntegrityError as err:
            raise OrderAlreadyExistsError(str(err))

        return CreateOrderResponse(response.model_dump())


class GetOrderByIDUseCase(UseCase, Resource):
    def execute(order_id: int) -> GetOrderByIDResponse:
        """
        Get order by its id
        """
        response = OrderRepository.get_order_by_id(order_id)

        return GetOrderByIDResponse(response.model_dump())


class GetAllOrdersUseCase(UseCaseNoRequest, Resource):
    def execute() -> GetAllOrdersResponse:
        """
        Get orders with filters
        """
        response = OrderRepository.get_all_orders()
        orders = [r.model_dump() for r in response]
        return GetAllOrdersResponse(orders)


class UpdateOrderStatusUseCase(UseCase, Resource):
    def execute(
        status: str,
        order_id: int,
    ) -> UpdateOrderResponse:
        """
        Update order status
        """
        try:
            response = OrderRepository.update_order_status(order_id, status)
        except IntegrityError as err:
            raise OrderUpdateError(str(err))

        return UpdateOrderResponse(response)
