from flask import Flask, render_template
from application.manager_setup import manager, db, User, Keys, Requests, Payments
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('application.config')

app.jinja_env.globals.update(zip=zip)

manager.init_app(app)
db.init_app(app)
mail = Mail()
mail.init_app(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
