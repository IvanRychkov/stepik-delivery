from flask import Blueprint, render_template

#
auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/account/')
def render_account():
    return render_template('account.html')


@auth.route('/auth/')
def render_auth():
    return render_template('auth.html')


@auth.route('/register/')
def render_ordered():
    return render_template('register.html')


@auth.route('/login/')
def render_login():
    return render_template('login.html')


@auth.route('/logout/')
def render_logout():
    return render_template('auth.html')
