from flask import Flask

from stepik_delivery.config import Config
from stepik_delivery.models import db


# Создание приложения
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных
# app.app_context().push()
db.init_app(app)

from stepik_delivery.views import *

