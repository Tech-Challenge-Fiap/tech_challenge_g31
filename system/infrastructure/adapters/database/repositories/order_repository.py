from typing import List
from sqlalchemy.exc import IntegrityError
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


class OrderRepository:
    @classmethod
    def create_order(cls, order: OrderEntity) -> OrderEntity:
        """Create order"""
        order_to_insert = OrderModel(
            price=order.price,
            status=order.status,
            waiting_time=order.waiting_time,
            payment_id=order.payment.id,
            client_id=order.client_id,
            order_date=order.order_date,
        )
        try:
            db.session.add(order_to_insert)
            db.session.commit()
        except Exception:
            raise IntegrityError()
        products_ids = [p.product_id for p in order.products]
        products = (
            db.session.query(ProductModel)
            .filter(ProductModel.product_id.in_(products_ids))
            .all()
        )
        # [ProductModel(**p.model_dump()) for p in order.products]
        product_map = {}
        for p in products:
            order_to_insert.products.append(p)
            product_map[p.product_id] = p
        try:
            db.session.add(order_to_insert)
            db.session.commit()
        except Exception:
            raise IntegrityError()
        order_products_to_update = []
        order_products = (
            db.session.query(OrderProductModel)
            .filter_by(order_id=order_to_insert.order_id)
            .all()
        )
        for op in order_products:
            p = product_map[op.product_id]
            op.type = p.type
            op.name = p.name
            op.price = p.price
            op.description = p.description
            order_products_to_update.append(op)
        try:
            db.session.add_all(order_products_to_update)
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
