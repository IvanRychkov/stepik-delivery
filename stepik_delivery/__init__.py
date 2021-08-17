import os

from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from stepik_delivery.auth import auth
from stepik_delivery.config import Config
from stepik_delivery.market import market
from stepik_delivery.models import db, Meal, Category, User, Order
from stepik_delivery.util.data import load_data

# Создание приложения
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY')

# Инициализация базы данных
with app.app_context():
    db.init_app(app)

    # Подключаем миграции
    migrate = Migrate(app, db)

    # Загружаем данные блюд и их категорий
    load_data()

    # Админка
    admin = Admin(app)
    # Добавим экраны работы с данными
    for model in Meal, Category, User, Order:
        admin.add_view(ModelView(model, db.session))

    # Подключаем блюпринты
    app.register_blueprint(market)
    app.register_blueprint(auth)
