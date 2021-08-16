from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

from stepik_delivery.models import db, Meal, User


class Account:
    LOGGED_IN = 'logged_in'

    def is_logged(self):
        """Проверяет наличие в сессии залогиненного пользователя."""
        return session.get(self.LOGGED_IN)

    def set_active_user(self, email):
        """Задаёт в сессии активного пользователя."""
        session[self.LOGGED_IN] = email

    def login(self, form):
        print('attempting login as', form.email.data)
        # Если юзер существует, и пароль верный:
        if form.validate_on_submit():
            # Логиним пользователя в сессию
            self.set_active_user(form.email.data)
            return User.query.filter(User.mail == form.email.data).first()

    def logout(self):
        """Удаляет пользователя из сессии."""
        return session.pop(self.LOGGED_IN)

    def register(self, form) -> User:
        """Добавляет пользователя в базу данных из формы."""
        try:
            if form.validate_on_submit():
                # Создаём пользователя
                new_user = User(
                    mail=form.email.data,
                    password=generate_password_hash(
                        form.password.data
                    )
                )
                db.session.add(new_user)
                db.session.commit()
                print('user added')
                # Логиним
                self.set_active_user(new_user.mail)
                return new_user
        except:
            print('user exists')
            db.session.rollback()


class Cart:
    """Интерфейс для взаимодействия с корзиной в сессии"""
    CART = 'cart'

    def get_content(self):
        """Возвращает id объектов в корзине"""
        cart_items = session.get(self.CART, [])
        if not cart_items:
            session.permanent = True
        return cart_items

    def get_meals(self):
        """Возвращает блюда из базы данных"""
        return [*map(Meal.query.get, self.get_content())]

    def add(self, product):
        """Добавляет товар в корзину"""
        if self.is_empty():
            session[self.CART] = []
        session[self.CART].append(product)
        # = temp_cart

    def remove(self, product):
        session[self.CART].remove(product)

    def is_empty(self):
        return not self.get_content()

    @staticmethod
    def reset():
        return session.pop('cart')
