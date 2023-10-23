from sqlalchemy.orm import relationship
from . import db

class ClientModel(db.Model):
    __tablename__ = 'clients'

    cpf = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    order = relationship("OrderModel", back_populates="client")

    def __init__(self, cpf, email, name):
        self.cpf = cpf
        self.email = email
        self.name = name