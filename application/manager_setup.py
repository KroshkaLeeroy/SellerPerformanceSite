from flask_login import LoginManager
from application.models import User, db
manager = LoginManager()


@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
