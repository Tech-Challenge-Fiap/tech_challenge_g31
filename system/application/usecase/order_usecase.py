from flask_restful import Resource
from psycopg2 import IntegrityError
from system.application.dto.requests.order_request import CreateOrderRequest
from system.application.dto.requests.payment_request import PaymentRequest
from system.application.dto.responses.order_response import (
    CreateOrderResponse,
    GetAllOrdersResponse,
    GetOrderByIDResponse,
    UpdateOrderResponse,
)
from system.application.exceptions.default_exceptions import InfrastructureError
from system.application.exceptions.order_exceptions import OrderDoesNotExistError, OrderUpdateError
from system.application.usecase.usecases import UseCase, UseCaseNoRequest
from system.domain.entities.order import OrderEntity
from system.domain.entities.payment import PaymentEntity
from system.domain.enums.enums import OrderStatusEnum, PaymentStatusEnum
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import NoObjectFoundError, PostgreSQLError
from system.infrastructure.adapters.database.repositories.order_repository import OrderRepository
from system.infrastructure.adapters.database.repositories.payment_repository import PaymentRepository
from system.infrastructure.adapters.database.repositories.product_repository import ProductRepository

class CreateOrderUseCase(UseCase, Resource):
    def execute(request: CreateOrderRequest) -> CreateOrderResponse:
        """
        Create Order
        """
        try:
            products = ProductRepository.get_products_by_ids(request.products)
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        except NoObjectFoundError:
            raise OrderDoesNotExistError
        order_price = 0
        order_waiting_time = 0
        for p in products:
            order_price += p.price
            order_waiting_time += p.prep_time
        try:
            payment = PaymentRepository.create_payment()
            order = OrderEntity(
                price=order_price,
                products_ids=request.products,
                waiting_time=order_waiting_time,
                client_id=request.client_cpf,
                payment=payment,
            )
            response = OrderRepository.create_order(order)
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        return CreateOrderResponse(response.model_dump())
    
class CheckoutOrderUseCase(UseCase, Resource):
    def execute(order_id: int, request:PaymentRequest) -> UpdateOrderResponse:
        try:
            order = OrderRepository.get_order_by_id(order_id = order_id)
            payment = PaymentRepository.update_payment(payment_id=order.payment.id, payment_status=request.status)
            order.payment = payment

            if payment.status == PaymentStatusEnum.PAID:
                updated_order_status = OrderStatusEnum.RECIEVED
            elif payment.status == PaymentStatusEnum.UNPAID:
                updated_order_status = OrderStatusEnum.CANCELED

            order = OrderRepository.update_order_status(order_id = order_id, status= updated_order_status)
        except IntegrityError as err:
            raise OrderUpdateError(str(err))
        except NoObjectFoundError:
            raise OrderDoesNotExistError
        return UpdateOrderResponse(order.model_dump())

class GetOrderByIDUseCase(UseCase, Resource):
    def execute(order_id: int) -> GetOrderByIDResponse:
        """
        Get order by its id
        """
        try:
            response = OrderRepository.get_order_by_id(order_id)
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))
        except NoObjectFoundError:
            raise OrderDoesNotExistError
        return GetOrderByIDResponse(response.model_dump())


class GetAllOrdersUseCase(UseCaseNoRequest, Resource):
    def execute() -> GetAllOrdersResponse:
        """
        Get orders with filters
        """
        try:
            response = OrderRepository.get_all_orders()
        except PostgreSQLError as err:
            raise InfrastructureError(str(err))

        orders = [r.model_dump() for r in response]
        return GetAllOrdersResponse(orders)


class UpdateOrderStatusUseCase(UseCase, Resource):
    def execute(
        status: OrderStatusEnum,
        order_id: int,
    ) -> UpdateOrderResponse:
        """
        Update order status
        """
        try:
            response = OrderRepository.update_order_status(order_id, status)
        except IntegrityError as err:
            raise OrderUpdateError(str(err))
        except NoObjectFoundError:
            raise OrderDoesNotExistError
        return UpdateOrderResponse(response.model_dump())
