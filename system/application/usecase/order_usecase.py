from flask_restful import Resource
from psycopg2 import IntegrityError
from system.application.dto.requests.order_request import CreateOrderRequest
from system.application.dto.responses.order_response import (
    CreateOrderResponse,
    GetAllOrdersResponse,
    GetOrderByIDResponse,
    UpdateOrderResponse,
)
from system.domain.entities.order import OrderEntity
from system.infrastructure.adapters.database.exceptions.order_exceptions import OrderAlreadyExistsError, OrderDoesNotExistError, OrderUpdateError

from system.infrastructure.adapters.database.repositories.order_repository import OrderRepository

class CreateOrderUseCase(Resource):
    def execute(
        request: CreateOrderRequest
    ) -> CreateOrderResponse:
        """
        Create order
        """
        order = OrderEntity(**request.model_dump())
        try:
            response = OrderRepository.create_order(order)
        except IntegrityError as err:
            raise OrderAlreadyExistsError(str(err))
       
        return CreateOrderResponse(response.model_dump())

class GetOrderByIDUseCase(Resource):
    def execute(
        order_id: int
    ) -> GetOrderByIDResponse:
        """
        Get order by its id
        """
        try:
            response = OrderRepository.get_order_by_id(order_id)
        except IntegrityError as err:
            raise OrderDoesNotExistError(str(err))
       
        return GetOrderByIDResponse(response.model_dump())
    
class GetAllOrdersUseCase(Resource):
    def execute(
    ) -> GetAllOrdersResponse:
        """
        Get orders with filters
        """
        try:
            response = OrderRepository.get_all_orders()
        except:
            raise IntegrityError
       
        return GetAllOrdersResponse(response)
    
class UpdateOrderStatusUseCase(Resource):
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