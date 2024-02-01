from flask import Blueprint, render_template
from flask_login import current_user

feedback_blueprint = Blueprint('feedback_blueprint', __name__)


@feedback_blueprint.route('/feedback')
def feedback_page():
    # TODO: Добавить в html отправку формы для обратной связи
    return render_template('feedback.html', user=current_user)
