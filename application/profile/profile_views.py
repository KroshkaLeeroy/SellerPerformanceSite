import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application.config import URL_TO_API
from application.setup import db, Requests, Keys
from application.utils import check_reports_from_API

profile_blueprint = Blueprint('profile_blueprint', __name__)


@profile_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    user = current_user
    req = Requests.query.get(user.id)
    keys = Keys.query.get(user.id)
    if request.method == 'POST':
        user.email = request.form.get('email')
        keys.api_key_seller = request.form.get('api_seller')
        keys.client_id_seller = request.form.get('client_id_seller')
        keys.api_key_performance = request.form.get('api_performance')
        keys.client_id_performance = request.form.get('client_id_performance')
        db.session.commit()

    return render_template('profile.html', user=user, req_c=req, keys=keys)


@profile_blueprint.route('/edit_profile')
@login_required
def edit_profile():
    req = Requests.query.get(current_user.id)
    keys = Keys.query.get(current_user.id)
    return render_template('edit_profile.html', user=current_user, req_c=req, keys=keys)


@profile_blueprint.route('/query', methods=['GET', 'POST'])
@login_required
def query_page():
    keys = Keys.query.get(current_user.id)
    if request.method == 'POST':
        date_from = request.form.get('date-from')
        date_to = request.form.get('date-to')
        data = {
            'user_id': keys.client_id_seller,
            'seller_secret': keys.api_key_seller,
            'seller_id': keys.client_id_seller,
            'perf_api': keys.api_key_performance,
            'perf_id': keys.client_id_performance,
            'date_from': date_from,
            'date_to': date_to,
        }
        # TODO: json check for Date values!
        if not date_to or not date_from:
            flash('Даты должны быть указаны!')
        else:
            try:
                response = requests.post(f'{URL_TO_API}/add-request', json=data)
                if response.status_code != 200:
                    flash('Нет возможности соединиться с сервером запросов')
                else:
                    flash('Запрос успешно отправлен на сервер')
            except Exception:
                flash('Нет возможности соединиться с сервером запросов')
            return redirect(url_for('profile_blueprint.query_page'))
    try:
        reports = check_reports_from_API(URL_TO_API, keys.client_id_seller)
    except requests.exceptions.ConnectionError as e:
        reports = [{
            'date_from': 'Нет возможности соединиться с сервером запросов',
            'date_to': '',
            'status': f'{e}',
        }]

    if keys.api_key_seller == '' or keys.api_key_performance == '':
        flash('Заполните ключи API')

    return render_template('query.html', reports=reports, user=current_user, URL=URL_TO_API)


@profile_blueprint.route('/history')
@login_required
def history_page():
    keys = Keys.query.get(current_user.id)
    try:
        reports = check_reports_from_API(URL_TO_API, keys.client_id_seller)
    except requests.exceptions.ConnectionError as e:
        reports = [{
            'date_from': 'Нет возможности соединиться с сервером запросов',
            'date_to': '',
            'status': f'{e}',
        }]

    return render_template('history.html', reports=reports, user=current_user, URL=URL_TO_API)


@profile_blueprint.after_request
def redirect_to_sign_in(response):
    if response.status_code == 401:
        return redirect(url_for('login_blueprint.login_page') + '?next=' + request.url)

    return response
