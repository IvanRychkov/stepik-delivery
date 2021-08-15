from datetime import datetime

from flask import Blueprint, render_template, session, redirect, request

from stepik_delivery.models import Meal, Category
from stepik_delivery.auth import account

market = Blueprint('market', __name__, template_folder='templates')


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
        session.pop('cart')


cart = Cart()


@market.route('/')
def render_main():
    cats = Category.query.all()
    return render_template('main.html',
                           cats=cats,
                           cart=cart)


@market.route('/cart/')
@market.route('/cart/<int:meal_id>/')
@market.route('/cart/remove/<int:meal_id>/')
@market.route('/cart/removed/')
def render_cart(meal_id=None):
    if meal_id:
        if '/remove/' in request.path:
            cart.remove(meal_id)
            return redirect('/cart/removed/')
        else:
            cart.add(meal_id)
        return redirect('/cart/')

    return render_template('cart.html',
                           cart=cart,
                           removed='removed' in request.path)


@market.route('/ordered/', methods=['POST'])
def render_ordered():
    """Добавляет заказ в базу данных."""
    account.login()
    # account.logout()
    return render_template('ordered.html')
