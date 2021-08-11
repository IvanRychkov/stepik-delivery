from flask import Flask
from flask_admin import Admin

from stepik_delivery.config import Config
from stepik_delivery.models import db
from stepik_delivery.market import market
from stepik_delivery.auth import auth


# Создание приложения
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных
# app.app_context().push()
db.init_app(app)

# Админка
admin = Admin(app)

# from stepik_delivery.views import *

app.register_blueprint(market)
app.register_blueprint(auth)
