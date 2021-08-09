from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(str(password))

    def validate_password(self, password):
        return check_password_hash(self.password_hash, str(password))


u = User()
u.password = 13
print(u.validate_password(10))
