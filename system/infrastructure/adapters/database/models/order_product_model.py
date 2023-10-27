from . import db
from sqlalchemy import Enum as SQLAlchemyEnum
from system.domain.enums.enums import ProductTypeEnum

class OrderProductModel(db.Model):
    __tablename__ = "orders_products"

    order_product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column("product_id", db.ForeignKey("products.product_id"))
    order_id = db.Column("order_id", db.ForeignKey("orders.order_id"))
    type = db.Column(SQLAlchemyEnum(ProductTypeEnum), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
