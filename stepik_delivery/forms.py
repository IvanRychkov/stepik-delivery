from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.fields import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, ValidationError, StopValidation

from stepik_delivery.models import User


def get_user(email):
    return User.query.filter(User.mail == email).first()


def user_exists(form, email):
    if get_user(email.data):
        raise StopValidation('Пользователь с такой почтой уже существует')


def user_not_exists(form, email):
    if not get_user(email.data):
        raise StopValidation('Пользователь с такой почтой не зарегистрирован')


def check_user_password(form, password):
    user = User.query.filter(User.mail == form.email.data).first()
    if not user:
        return
    if not check_password_hash(user.password, password.data):
        raise ValidationError('Неверный пароль')


class AuthForm(FlaskForm):
    email = EmailField('Электропочта', [InputRequired(), user_not_exists])
    password = PasswordField('Пароль', [InputRequired(),
                                        check_user_password])


class RegisterForm(AuthForm):
    # Переопределяем поля с паролем
    email = EmailField('Электропочта', [InputRequired(), user_exists])
    password = PasswordField('Пароль', [InputRequired(),
                                        Length(min=5,
                                               message='Пароль должен быть не короче 5 символов')])


class OrderForm(FlaskForm):
    pass
