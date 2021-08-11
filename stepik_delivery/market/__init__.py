from flask import Blueprint, render_template


market = Blueprint('market', __name__, template_folder='templates')


@market.route('/')
def render_main():
    return render_template('main.html')


@market.route('/cart/')
def render_cart():
    return render_template('cart.html')


@market.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')