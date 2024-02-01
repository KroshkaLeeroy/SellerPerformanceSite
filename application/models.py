from flask_login import UserMixin
from application.db_setup import db


class User(db.Model, UserMixin):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)

    email = db.Column(db.String(128), default='')
    api_key_seller = db.Column(db.String(255), default='')
    client_id_seller = db.Column(db.String(255), default='')

    api_key_performance = db.Column(db.String(255), default='')
    client_id_performance = db.Column(db.String(255), default='')

    account_type = db.Column(db.String(128), default='')
    request_count = db.Column(db.Integer, default=0)

    account_status = db.Column(db.String(128), default='active')




