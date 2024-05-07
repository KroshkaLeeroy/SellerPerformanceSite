from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), default='')
    password = db.Column(db.String(255), nullable=False)
    is_account_active = db.Column(db.Boolean, default=True)
    account_type = db.Column(db.String(128), default='')

    keys = db.relationship("Keys", back_populates="parent")
    requests = db.relationship("Requests", back_populates="parent")
    payments = db.relationship("Payments", back_populates="parent")


class Keys(db.Model):
    __tablename__ = 'keys_table'

    parent_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), primary_key=True, autoincrement=True)
    parent = db.relationship("User", back_populates="keys")

    api_key_seller = db.Column(db.String(255), default='')
    client_id_seller = db.Column(db.String(255), default='')
    api_key_performance = db.Column(db.String(255), default='')
    client_id_performance = db.Column(db.String(255), default='')


class Requests(db.Model):
    __tablename__ = 'requests_table'

    parent_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), primary_key=True, autoincrement=True)
    parent = db.relationship("User", back_populates="requests")

    request_count = db.Column(db.Integer, default=0)


class Payments(db.Model):
    __tablename__ = 'payments_table'

    parent_id = db.Column(db.Integer, db.ForeignKey("user_table.id"), primary_key=True, autoincrement=True)
    parent = db.relationship("User", back_populates="payments")

    plan = db.Column(db.String(128), default='trial')
    is_plan_active = db.Column(db.Boolean, default=True)
    autopay = db.Column(db.Boolean, default=False)
    shops_connected = db.Column(db.Integer, default=0)
    payment_date = db.Column(db.DateTime)
