from flask import Blueprint, render_template, session, redirect, request
from stepik_delivery.forms import AuthForm, RegisterForm
from stepik_delivery.util import account, cart

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/account/')
def render_account():
    return render_template('account.html',
                           cart=cart)


@auth.route('/auth/')
def render_auth():
    form = AuthForm()
    return render_template('auth.html',
                           form=form)


@auth.route('/register/', methods=['GET', 'POST'])
def render_ordered():
    # Если пользователь залогинен, сразу отправляем в ЛК
    if account.is_logged():
        return redirect('/account/')

    # Создаём/заполняем форму
    form = RegisterForm()

    # Если выполняем регистрацию
    if request.method == 'POST':
        # Аккаунт пробует зарегистрироваться в базе
        account.register(form)

        # Проверяем регистрацию
        if account.is_logged():
            # Направляем пользователя в личный кабинет
            return redirect('/account/')
        else:
            return redirect('/register/')

    return render_template('register.html',
                           form=form)


@auth.route('/login/', methods=['POST'])
def render_login():
    form = AuthForm()
    account.login(form.email.data)

    return render_template('account.html')


@auth.route('/logout/')
def render_logout():
    account.logout()
    return redirect('/auth/')
