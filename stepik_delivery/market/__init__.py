from datetime import datetime

from flask import Blueprint, render_template, session, redirect, request

from stepik_delivery.models import Category
from stepik_delivery.util import account, cart

market = Blueprint('market', __name__, template_folder='templates')


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
