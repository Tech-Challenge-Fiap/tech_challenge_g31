from typing import List
from psycopg2 import IntegrityError
from system.domain.entities.order import OrderEntity
from system.infrastructure.adapters.database.exceptions.order_exceptions import OrderDoesNotExistError
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.order_model import OrderModel


class OrderRepository:

    @staticmethod
    def create_order(order: OrderEntity) -> OrderEntity:
        """ Create order """
        order_to_insert = OrderModel(**order.model_dump())
        order_to_insert.type = str(order_to_insert.type).split(".")[1]
        try:
            db.session.add(order_to_insert)
            db.session.commit()
        except:
            raise IntegrityError()
        inserted_order = db.session.query(OrderModel).filter_by(name=order.name).first()
        return OrderEntity(**inserted_order.__dict__)
    
    @staticmethod
    def get_order_by_id(order_id: int) -> OrderEntity:
        """ Get a order by it's id """
        order = db.session.query(OrderModel).filter_by(order_id=order_id).first()
        return OrderEntity.from_orm(order)
    
    @staticmethod
    def get_all_orders() -> List[OrderEntity]:
        """ Get all orders """
        orders = db.session.query(OrderModel).all()
        orders_list = [OrderEntity.from_orm(order) for order in orders]
        return orders_list
    
    @staticmethod
    def update_order_status(order_id: int, status:str) -> OrderEntity:
        """ Update an order's status """
        try:
            order = db.session.query(OrderModel).filter_by(order_id=order_id).first()
        except IntegrityError as err:
            raise OrderDoesNotExistError(str(err))
        try:
            db.session.query(OrderModel).filter_by(order_id=order_id).update(status=status)
            db.session.commit()
        except:
            raise IntegrityError()

        return OrderEntity(**order.__dict__)