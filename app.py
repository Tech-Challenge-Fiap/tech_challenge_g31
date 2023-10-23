import os
from flask import Flask, request
from flask_migrate import Migrate
from psycopg2 import IntegrityError
from system.application.dto.requests.client_request import CreateClientRequest
from system.application.dto.requests.order_request import CreateOrderRequest, UpdateOrderStatusRequest
from system.application.dto.requests.product_request import CreateProductRequest, UpdateProductRequest
from system.application.usecase.client_usecase import CreateClientUseCase, GetAllClientsUseCase, GetClientByCPFUseCase
from system.application.usecase.order_usecase import CreateOrderUseCase, GetAllOrdersUseCase, GetOrderByIDUseCase, UpdateOrderStatusUseCase
from system.application.usecase.products_usecase import CreateProductUseCase, DeleteProductUseCase, GetAllProductsUseCase, GetProductByIDUseCase, GetProductsByTypeUseCase, UpdateProductUseCase
from system.infrastructure.adapters.database.exceptions.client_exceptions import ClientAlreadyExistsError, ClientDoesNotExistError
from system.infrastructure.adapters.database.exceptions.order_exceptions import OrderAlreadyExistsError, OrderDoesNotExistError
from system.infrastructure.adapters.database.exceptions.product_exceptions import ProductAlreadyExistsError, ProductDoesNotExistError  # Importe o Flask-Migrate


app = Flask(__name__)

db_name = os.environ["POSTGRES_DB"]
db_user = os.environ["POSTGRES_USER"]
db_pass = os.environ["POSTGRES_PASSWORD"]
db_host = os.environ["POSTGRES_HOST"]
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'
#postgresql://username:password@host:port/database_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from system.infrastructure.adapters.database.models import *

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def hello():
    return '<h1>Hello, Munds!</h1>'

if __name__ == '__main__':
    app.run()

#Importing views
from system.adapters_entrypoints.api.routes import client_views, product_views, order_views

#Product

# #Order

# #Payment

# #Old Order (OrderProduct)
