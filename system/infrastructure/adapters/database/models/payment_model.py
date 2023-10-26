from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from system.domain.enums.enums import PaymentStatusEnum
from . import db

class PaymentModel(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qr_code = db.Column(db.String, nullable=False)
    payed_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    status = db.Column(SQLAlchemyEnum(PaymentStatusEnum), nullable=False)
    order = relationship("OrderModel", back_populates="payment", uselist=False)