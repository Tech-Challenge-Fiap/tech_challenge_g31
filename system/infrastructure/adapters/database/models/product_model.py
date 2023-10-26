from . import db


class ProductModel(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer)
    prep_time = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String, nullable=True)
