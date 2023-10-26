from . import db


class OrderProductModel(db.Model):
    __tablename__ = "orders_products"

    order_product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column("product_id", db.ForeignKey("products.product_id"))
    order_id = db.Column("order_id", db.ForeignKey("orders.order_id"))
    type = db.Column(db.String(10), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
