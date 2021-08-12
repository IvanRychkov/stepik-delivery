from flask import Blueprint, render_template, session, redirect
from stepik_delivery.models import Meal, Category

market = Blueprint('market', __name__, template_folder='templates')


class Cart:
    """Интерфейс для взаимодействия с корзиной в сессии"""
    CART = 'cart'

    def get_content(self):
        return session.get(self.CART, [])

    def add(self, product):
        """Добавляет товар в корзину"""
        temp_cart = self.get_content()
        if product in temp_cart:
            return

        temp_cart.append(product)
        session[self.CART] = temp_cart

    def is_empty(self):
        return not self.get_content()


cart = Cart()


@market.route('/')
def render_main():
    cats = Category.query.all()
    return render_template('main.html',
                           cats=cats)


@market.route('/cart/')
@market.route('/cart/<int:meal_id>/')
def render_cart(meal_id=None):
    if meal_id:
        cart.add(meal_id)
        return redirect('/cart/')

    if cart.get_content():
        meals = Meal.query.filter(Meal.id.in_(cart.get_content())).all()
        return render_template('cart.html', meals=meals)


@market.route('/ordered/')
def render_ordered():
    """Добавить заказ в базу данных"""
    return render_template('ordered.html')