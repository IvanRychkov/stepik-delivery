from flask import Blueprint, render_template, session, redirect
from stepik_delivery.forms import AuthForm

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


@auth.route('/register/')
def render_ordered():
    return render_template('register.html')


@auth.route('/login/', methods=['POST'])
def render_login():
    form = AuthForm()
    account.login()
    print(form.email.data, form.password.data)

    return render_template('account.html')


@auth.route('/logout/')
def render_logout():
    account.logout()
    return redirect('/auth/')
