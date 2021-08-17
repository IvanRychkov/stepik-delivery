from flask import Blueprint, render_template, session, redirect, request
from stepik_delivery.forms import AuthForm, RegisterForm
from stepik_delivery.util import account, cart

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/account/')
def render_account():
    # Если не залогинен, то отправляем логиниться
    if not account.current_user():
        return redirect('/auth/')
    return render_template('account.html',
                           cart=cart,
                           account=account)


@auth.route('/auth/', methods=['GET', 'POST'])
def render_auth():
    # Если пользователь чудом попал на страницу логина,
    # Сразу его перебрасываем в аккаунт
    if account.current_user():
        return redirect('/account/')

    # Создаём/заполняем форму
    form = AuthForm()

    # Если POST
    if request.method == 'POST':
        # Пробуем залогинить аккаунт
        if account.login(form):
            # В случае успеха
            return redirect('/account/')

    return render_template('auth.html',
                           form=form)


@auth.route('/register/', methods=['GET', 'POST'])
def render_ordered():
    # Если пользователь залогинен, сразу отправляем в ЛК
    if account.current_user():
        return redirect('/account/')

    # Создаём/заполняем форму
    form = RegisterForm()

    # Если выполняем регистрацию
    if request.method == 'POST':
        if form.validate_on_submit():
            # Аккаунт пробует зарегистрироваться в базе
            account.register(form)

            # Проверяем регистрацию
            if account.current_user():
                # Направляем пользователя в личный кабинет
                return redirect('/account/')
            return redirect('/register/')

    return render_template('register.html',
                           form=form)


@auth.route('/logout/')
def render_logout():
    account.logout()
    return redirect('/auth/')
