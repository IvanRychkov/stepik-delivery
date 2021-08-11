from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    mail = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)


orders_meals = db.Table(
    'orders_meals',
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')),
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'))
)


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String())
    picture = db.Column(db.String())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='meals', uselist=False)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    meals = db.relationship(Meal, back_populates='category')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String())
    mail = db.Column(db.String(), db.ForeignKey('users.mail'))
    user = db.relationship('User', backref=db.backref('orders'))
    phone = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    meals = db.relationship(Meal, secondary=orders_meals,
                            backref=db.backref('orders'))
