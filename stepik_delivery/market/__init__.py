from datetime import datetime

from flask import Blueprint, render_template, redirect, request

from stepik_delivery.forms import OrderForm
from stepik_delivery.models import db, Category, Order
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
    # Если есть meal_id, то делаем действие с блюдом
    if meal_id:
        if '/remove/' in request.path:
            cart.remove(meal_id)
            return redirect('/cart/removed/')
        else:
            cart.add(meal_id)
        return redirect('/cart/')

    # Если юзер залогинен, то в форму подтянется его почта
    form = OrderForm(email=account.current_user())

    return render_template('cart.html',
                           cart=cart,
                           form=form,
                           removed='removed' in request.path)


@market.route('/ordered/', methods=['POST'])
def render_ordered():
    """Добавляет заказ в базу данных."""
    # Создаём форму из POST-запроса
    form = OrderForm()

    # Создаём объект заказа в базе данных
    meals = cart.get_meals()
    new_order = Order(date=datetime.now(),
                      amount=sum(map(lambda m: m.price,
                                     meals)),
                      status='in progress',
                      mail=form.email.data,
                      phone=form.phone.data,
                      address=form.address.data,
                      meals=meals
                      )
    print(new_order.meals)
    db.session.add(new_order)
    db.session.commit()

    cart.reset()
    return render_template('ordered.html',
                           account=account)
