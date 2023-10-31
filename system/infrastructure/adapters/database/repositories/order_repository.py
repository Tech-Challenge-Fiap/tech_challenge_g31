from collections import Counter
from typing import List
from sqlalchemy.exc import IntegrityError
from system.application.exceptions.order_exceptions import OrderUpdateError
from system.application.ports.order_port import OrderPort
from system.domain.entities.order import OrderEntity
from system.domain.entities.product import BasicProductEntity
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
        try:
            products = (
                db.session.query(ProductModel)
                .filter(ProductModel.product_id.in_(order.products_ids))
                .all()
            )
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        #Counts how many times each product was ordered
        product_count = Counter(order.products_ids)
        order_products = []
        # THIS FOR IS GETTING PRODUCT ON BY ONE AND APPENDING IN ORDER_PRODUCT
        for product_data in products:
            order_product = OrderProductModel(
                order_id=order_to_insert.order_id,
                product_id=product_data.product_id,
                type=product_data.type,
                name=product_data.name,
                price=product_data.price,
                description=product_data.description,
                quantity=product_count[product_data.product_id]
            )
            order_products.append(order_product)
        try:
            db.session.add_all(order_products)
            db.session.commit()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        
        order_to_insert.products_ids = order.products_ids
        return OrderEntity.from_orm(order_to_insert)

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
            product_list.append(BasicProductEntity.from_orm(product))
        order_dict = order.__dict__
        order_dict["payment"] = order.payment
        order_dict["products"] = product_list
        return OrderEntity.from_orm(order_dict)

    @classmethod
    def get_all_orders(cls) -> List[OrderEntity]:
        """Get all orders"""
        try:
            orders = db.session.query(OrderModel).all()
        except IntegrityError:
            raise PostgreSQLError("PostgreSQL Error")
        orders_dict = []
        for order in orders:
            try:
                order_products = db.session.query(OrderProductModel).filter_by(order_id=order.order_id).all()
            except IntegrityError:
                raise PostgreSQLError("PostgreSQL Error")
            product_list = []
            for product in order_products:
                product_list.append(BasicProductEntity.from_orm(product))
            order_dict = order.__dict__
            order_dict["payment"] = order.payment
            order_dict["products"] = product_list
            orders_dict.append(order_dict)
        orders_list = [OrderEntity.from_orm(order) for order in orders_dict]
        return orders_list

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
            for _ in range(product.quantity):
                product_list.append(product.product_id)
        if not order:
            raise NoObjectFoundError
        try:
            order.status = status
            db.session.commit()
        except IntegrityError:
            raise OrderUpdateError
        order.products_ids = product_list
        return OrderEntity.from_orm(order)