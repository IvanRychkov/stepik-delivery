import os

import pandas as pd
from sqlalchemy.exc import IntegrityError

from stepik_delivery.models import db

DATA_PATH = 'stepik_delivery/util/data/'


def load_csv(data, tablename):
    """Загружает датафрейм pandas в таблицу через SQLAlchemy."""
    try:
        # Пробуем загрузить данные в таблицу
        data.to_sql(tablename, con=db.engine, if_exists='append')
        db.session.commit()
    except:
        # Если нарушен констрейнт уникальности, отменяем операцию
        db.session.rollback()


def load_data():
    # Считываем csv
    meals = pd.read_csv(os.path.join(DATA_PATH, 'delivery_items.csv'), index_col=0)
    categories = pd.read_csv(os.path.join(DATA_PATH, 'delivery_categories.csv'), index_col=0)

    # Загружвем в базу
    for table, name in zip([meals, categories],
                           ['meals', 'categories']):
        load_csv(table, name)
