from flask import Blueprint, render_template
from flask_login import current_user

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route('/')
def main_page():
    return render_template('main.html', user=current_user)
