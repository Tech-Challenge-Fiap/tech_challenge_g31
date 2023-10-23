from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import db

class OrderModel(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    price = db.Column(db.Integer)
    status = db.Column(db.String(10), nullable=False)
    waiting_time = db.Column(db.Integer)
    client_id = db.Column(db.String, db.ForeignKey('clients.cpf'), nullable=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    client = relationship("ClientModel", back_populates="order")
    payment = relationship("PaymentModel", back_populates="order")
    products = relationship(
        "ProductModel", secondary="orders_products"
    )
