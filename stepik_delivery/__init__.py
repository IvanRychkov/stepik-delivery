from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin

from stepik_delivery.auth import auth
from stepik_delivery.config import Config
from stepik_delivery.market import market
from stepik_delivery.models import db, Meal
from stepik_delivery.util.data.data_loader import load_data

# Создание приложения
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных
with app.app_context():
    db.init_app(app)

    migrate = Migrate(app, db)


    # Админка
    admin = Admin(app)

    # from stepik_delivery.views import *

    app.register_blueprint(market)
    app.register_blueprint(auth)

    # Загружаем данные блюд и их категорий
    load_data()
