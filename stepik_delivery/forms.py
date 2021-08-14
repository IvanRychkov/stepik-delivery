from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email
from wtforms.fields import PasswordField, StringField
from wtforms.fields.html5 import EmailField


class AuthForm(FlaskForm):
    email = EmailField('Электропочта', [InputRequired()])
    password = PasswordField('Пароль', [InputRequired()])
