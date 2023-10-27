import os
from flask import Flask, request
from flask_migrate import Migrate

app = Flask(__name__)

# db_name = os.environ["POSTGRES_DB"]
# db_user = os.environ["POSTGRES_USER"]
# db_pass = os.environ["POSTGRES_PASSWORD"]
# db_host = os.environ["POSTGRES_HOST"]
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@localhost/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://myappuser:myapppassword@localhost/myappdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://myappuser:myapppassword@localhost/myappdb'
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
