import os

import pandas as pd
from sqlalchemy.exc import IntegrityError

from stepik_delivery.models import db, Meal, Category

DATA_PATH = 'stepik_delivery/util/'


def load_csv(filename, model):
    """Загружает датафрейм pandas в таблицу через SQLAlchemy."""
    try:
        # Считаем файл
        for i, row in pd.read_csv(os.path.join(DATA_PATH, filename)).iterrows():
            db.session.add(model(**row.to_dict()))
            # print(row.to_dict())
        db.session.commit()
    except:
        # Если ошибка, отменяем операцию
        db.session.rollback()


def load_data():
    # Считываем csv
    for file, model in zip(['delivery_items.csv', 'delivery_categories.csv'],
                           [Meal, Category]):
        print('loading', file)
        # Загружвем в базу
        load_csv(file, model)
