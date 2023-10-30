from typing import List
from sqlalchemy.exc import IntegrityError
from system.application.exceptions.order_exceptions import OrderUpdateError
from system.application.ports.order_port import OrderPort
from system.domain.entities.order import OrderEntity, OrderProductEntity
from system.domain.enums.enums import OrderStatusEnum
from system.infrastructure.adapters.database.exceptions.postgres_exceptions import NoObjectFoundError, PostgreSQLError
from system.infrastructure.adapters.database.models import db
from system.infrastructure.adapters.database.models.order_model import OrderModel
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

        try:
            # CREATING ORDER IN DATABASE
            # FLUSH TO REFRESH order_to_insert WITH ORDER_ID
            db.session.add(order_to_insert)
            db.session.commit()
            db.session.flush()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
            # GETTING PRODUCTS TO POPULATE ORDER 
        products_ids = [p.product_id for p in order.products]
        try:
            products = (
                db.session.query(ProductModel)
                .filter(ProductModel.product_id.in_(products_ids))
                .all()
            )
            products_map = {p.product_id: p for p in products}
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        order_products_to_insert = []
        order_products_entities = []
        # THIS FOR IS GETTING PRODUCT ON BY ONE AND APPENDING IN ORDER_PRODUCT
        for product_to_order in order.products:
            product_data = products_map.get(product_to_order.product_id)
            order_product = OrderProductModel(
                order_id=order_to_insert.order_id,
                product_id=product_data.product_id,
                type=product_data.type,
                name=product_data.name,
                price=product_data.price,
                description=product_data.description,
                quantity=product_to_order.quantity
            )
            order_products_to_insert.append(order_product)
            order_products_entities.append(OrderProductEntity.from_orm(order_product))
        try:
            db.session.add_all(order_products_to_insert)
            db.session.commit()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        
        response = OrderEntity.from_orm(order_to_insert)
        response.products = order_products_entities
        return response

    @classmethod
    def get_order_by_id(cls, order_id: int) -> OrderEntity:
        """Get a order by it's id"""
        try:
            order = db.session.query(OrderModel).filter_by(order_id=order_id).first()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        if not order:
            raise NoObjectFoundError
        try:
            order_products = db.session.query(OrderProductModel).filter_by(order_id=order_id).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        product_list = []
        for product in order_products:
            product_list.append(OrderProductEntity.from_orm(product))
        response = OrderEntity.from_orm(order)
        response.products = product_list
        return response

    @classmethod
    def get_all_orders(cls) -> List[OrderEntity]:
        """Get all orders"""
        try:
            orders = db.session.query(OrderModel).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        
        response = []
        for order in orders:
            try:
                order_products = db.session.query(OrderProductModel).filter_by(order_id=order.order_id).all()
            except IntegrityError:
                raise PostgreSQLError("PostgreSQL Error")
            product_list = []
            for product in order_products:
                product_list.append(OrderProductEntity.from_orm(product))
            order_entity = OrderEntity.from_orm(order)
            order_entity.products = product_list
            response.append(order_entity)

        return response

    @classmethod
    def update_order_status(cls, order_id: int, status: OrderStatusEnum) -> OrderEntity:
        """Update an order's status"""
        try:
            order = db.session.query(OrderModel).filter_by(order_id=order_id).first()
            order_products = db.session.query(OrderProductModel).filter_by(order_id=order_id).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        product_list = []
        for product in order_products:
            product_list.append(OrderProductEntity.from_orm(product))
        if not order:
            raise NoObjectFoundError
        try:
            order.status = status
            db.session.commit()
        except IntegrityError:
            raise OrderUpdateError
        response = OrderEntity.from_orm(order)
        response.products = product_list
        return response