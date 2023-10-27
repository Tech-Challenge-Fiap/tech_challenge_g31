from abc import abstractmethod
from typing import List
from system.domain.enums.enums import OrderStatusEnum
from system.application.dto.requests.order_request import CreateOrderRequest

from system.domain.entities.order import OrderEntity


class OrderPort:
    @classmethod
    @abstractmethod
    def create_order(payload: CreateOrderRequest) -> OrderEntity:
        """
        Method that create order
        """

    @classmethod
    @abstractmethod
    def get_all_orders(status: OrderStatusEnum) -> List[OrderEntity]:
        """
        Method thar gets all orders by status
        """

    @classmethod
    @abstractmethod
    def get_order_by_id(order_id) -> OrderEntity:
        """
        Get a order by it's id
        """

    @classmethod
    @abstractmethod
    def update_order_status(order_id) -> OrderEntity:
        """
        Update an order's status
        """
