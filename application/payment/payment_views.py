from flask import Blueprint, render_template
from flask_login import current_user

payment_blueprint = Blueprint('payment_blueprint', __name__)


@payment_blueprint.route('/payment')
def payment_page():
    return render_template('payments.html', user=current_user)
