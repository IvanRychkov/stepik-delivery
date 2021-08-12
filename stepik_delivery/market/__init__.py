from flask import Blueprint, render_template, session, redirect, current_app
from stepik_delivery.models import Meal, Category

market = Blueprint('market', __name__, template_folder='templates')


class Cart:
    """Интерфейс для взаимодействия с корзиной в сессии"""
    CART = 'cart'

    def get_content(self):
        """Возвращает id объектов в корзине"""
        if not self.session.get(self.CART, []):
            self.session.permanent = True
        return self.session.get(self.CART, [])

    def get_meals(self):
        """Возвращает блюда из базы данных"""
        return [*map(Meal.query.get, self.get_content())]

    def add(self, product):
        """Добавляет товар в корзину"""
        temp_cart = self.get_content()
        if product in temp_cart:
            return

        temp_cart.append(product)
        self.session[self.CART] = temp_cart

    def is_empty(self):
        return not self.get_content()

    def __init__(self, session):
        self.session = session


cart = Cart(session)


@market.route('/')
def render_main():
    cats = Category.query.all()
    return render_template('main.html',
                           cats=cats,
                           cart=cart)


@market.route('/cart/')
@market.route('/cart/<int:meal_id>/')
def render_cart(meal_id=None):
    if meal_id:
        cart.add(meal_id)
        return redirect('/cart/')

    return render_template('cart.html', cart=Cart(session))


@market.route('/ordered/')
def render_ordered():
    """Добавить заказ в базу данных"""
    return render_template('ordered.html')