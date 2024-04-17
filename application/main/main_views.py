import requests
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from application.config import URL_TO_API
from application.utils import check_reports_from_API

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route('/')
def main_page():
    if current_user.is_authenticated:
        try:
            reports = check_reports_from_API(URL_TO_API, current_user.client_id_seller)
        except requests.exceptions.ConnectionError as e:
            reports = [{
                'date_from': 'Нет возможности соединиться с сервером запросов',
                'date_to': '',
                'status': f'{e}',
            }]

        return render_template('main.html', reports=reports, user=current_user, URL=URL_TO_API)
    else:
        return redirect(url_for('login_blueprint.login_page'))


@main_blueprint.route('/yandex_<variable>.html')
def yandex_page(variable):
    return render_template(f'yandex_{variable}.html')
