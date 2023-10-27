from typing import List
from sqlalchemy.exc import IntegrityError
from system.application.ports.order_port import OrderPort
from system.domain.entities.order import OrderEntity
from system.infrastructure.adapters.database.exceptions.order_exceptions import (
    OrderDoesNotExistError,
)
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.order_model import OrderModel
from system.infrastructure.adapters.database.exceptions.order_exceptions import OrderUpdateError
from system.infrastructure.adapters.database.models.order_product_model import (
    OrderProductModel,
)
from system.infrastructure.adapters.database.models.product_model import ProductModel


class OrderRepository(OrderPort):
    @classmethod
    def create_order(cls, order: OrderEntity) -> OrderEntity:
        # ORDER MODEL PAYLOAD CREATE
        order_to_insert = OrderModel(
            price=order.price,
            status=order.status,
            waiting_time=order.waiting_time,
            payment_id=order.payment.id,
            client_id=order.client_id,
            order_date=order.order_date,
        )

        # GETTING PRODUCTS TO POPULATE ORDER 
        products = (
            db.session.query(ProductModel)
            .filter(ProductModel.product_id.in_(order.products_ids))
            .all()
        )

        # THIS FOR IS GETTING PRODUCT ON BY ONE AND APPENDING IN ORDER_PRODUCT
        for product_data in products:
            product = product_data
            op_type = product_data.type
            op_name = product_data.name
            op_price = product_data.price
            op_description = product_data.description

            order_to_insert.products.append(product, type=op_type, name=op_name, price=op_price, description=op_description)

        # THIS TRY CREATE THE NEW ORDER AND THE ORDER_PRODUCTS
        try:
            db.session.add(order_to_insert)
            db.session.commit()
        except Exception:
            raise IntegrityError()
        
        return OrderEntity.from_orm(order_to_insert)

    @classmethod
    def get_order_by_id(cls, order_id: int) -> OrderEntity:
        """Get a order by it's id"""
        order = db.session.query(OrderModel).filter_by(order_id=order_id).first()
        if not order:
            raise OrderDoesNotExistError
        return OrderEntity.from_orm(order)

    @classmethod
    def get_all_orders(cls) -> List[OrderEntity]:
        """Get all orders"""
        orders = db.session.query(OrderModel).all()
        orders_list = [OrderEntity.from_orm(order) for order in orders]
        return orders_list

    @classmethod
    def update_order_status(cls, order_id: int, status: str) -> OrderEntity:
        """Update an order's status"""
        order = db.session.query(OrderModel).filter_by(order_id=order_id).first()
        if not order:
            raise OrderDoesNotExistError
        try:
            db.session.query(OrderModel).filter_by(order_id=order_id).update(
                status=status
            )
            db.session.commit()
        except IntegrityError:
            raise OrderUpdateError

        return OrderEntity(**order.__dict__)
