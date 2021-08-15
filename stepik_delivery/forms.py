from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from wtforms.fields import PasswordField
from wtforms.fields.html5 import EmailField


class AuthForm(FlaskForm):
    email = EmailField('Электропочта', [InputRequired()])
    password = PasswordField('Пароль', [InputRequired()])


class RegisterForm(AuthForm):
    # Переопределяем поле с паролем
    password = PasswordField('Пароль', [InputRequired(), Length(min=5)])


class OrderForm(FlaskForm):
    pass
