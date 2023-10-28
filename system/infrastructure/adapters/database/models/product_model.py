from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from system.domain.enums.enums import ProductTypeEnum
from . import db


class ProductModel(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(SQLAlchemyEnum(ProductTypeEnum), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer)
    prep_time = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
