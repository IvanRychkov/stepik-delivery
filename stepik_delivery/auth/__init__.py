from flask import Blueprint, render_template, session, redirect, request
from stepik_delivery.forms import AuthForm, RegisterForm
from stepik_delivery.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

#
auth = Blueprint('auth', __name__, template_folder='templates')


class Account:
    LOGGED_IN = 'logged_in'

    def is_logged(self):
        return session.get(self.LOGGED_IN)

    def login(self):
        session[self.LOGGED_IN] = True

    def logout(self):
        session.pop(self.LOGGED_IN)


account = Account()


@auth.route('/account/')
def render_account():
    return render_template('account.html')


@auth.route('/auth/')
def render_auth():
    form = AuthForm()
    return render_template('auth.html',
                           form=form)


@auth.route('/register/', methods=['GET', 'POST'])
def render_ordered():
    # Создаём/заполняем форму
    form = RegisterForm()

    if request.method == 'POST':
        # Если выполняем регистрацию
        try:
            # if form.validate_on_submit():
            new_user = User(
                mail=form.email.data,
                password=generate_password_hash(
                    form.password.data
                )
            )
            db.session.add(new_user)
            print('user added')
            db.session.commit()
            return redirect('/account/')
        except:
            db.session.rollback()

    return render_template('register.html',
                           form=form)


@auth.route('/login/', methods=['POST'])
def render_login():
    form = AuthForm()
    account.login()

    return render_template('account.html')


@auth.route('/logout/')
def render_logout():
    account.logout()
    return redirect('/auth/')
