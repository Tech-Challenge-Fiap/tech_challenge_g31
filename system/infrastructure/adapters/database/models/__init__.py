from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from system.infrastructure.adapters.database.models.client_model import ClientModel
from system.infrastructure.adapters.database.models.order_model import OrderModel
from system.infrastructure.adapters.database.models.order_product_model import OrderProductModel
from system.infrastructure.adapters.database.models.payment_model import PaymentModel
from system.infrastructure.adapters.database.models.product_model import ProductModel