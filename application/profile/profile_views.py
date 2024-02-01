import requests

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application.config import URL_TO_API
from application.setup import db

profile_blueprint = Blueprint('profile_blueprint', __name__)


@profile_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    user = current_user
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.api_key_seller = request.form.get('api_seller')
        user.client_id_seller = request.form.get('client_id_seller')
        user.api_key_performance = request.form.get('api_performance')
        user.client_id_performance = request.form.get('client_id_performance')

        db.session.commit()

    return render_template('profile.html', user=user)


@profile_blueprint.route('/edit_profile')
@login_required
def edit_profile():
    return render_template('edit_profile.html', user=current_user)


@profile_blueprint.route('/query', methods=['GET', 'POST'])
@login_required
def query_page():
    if request.method == 'POST':
        date_from = request.form.get('date-from')
        date_to = request.form.get('date-to')
        data = {
            'email': current_user.email,
            'api_key_seller': current_user.api_key_seller,
            'client_id_seller': current_user.client_id_seller,
            'api_key_performance': current_user.api_key_performance,
            'client_id_performance': current_user.client_id_performance,
            'date_from': date_from,
            'date_to': date_to,
        }
        if not date_to or not date_from:
            flash('Даты должны быть указаны!')
        else:
            response = requests.post(f'{URL_TO_API}/add-request', json=data)
    try:
        existing_reports = requests.get(f'{URL_TO_API}/check-pull/{current_user.email}')
        if existing_reports.status_code == 200:
            reports = existing_reports.json()
        else:
            reports = []
    except requests.exceptions.ConnectionError as e:
        reports = [{
            'date_from': 'Нет возможности соединиться с сервером запросов',
            'date_to': '',
            'status': f'{e}',
        }]

    user = current_user
    if user.api_key_seller == '' or user.api_key_performance == '':
        flash('Заполните ключи API!')

    return render_template('query.html', requests=reports, user=current_user)


@profile_blueprint.route('/history')
@login_required
def history_page():
    try:
        existing_reports = requests.get(f'{URL_TO_API}/check-pull/{current_user.email}')
        if existing_reports.status_code == 200:
            reports = existing_reports.json()
        else:
            reports = []
    except requests.exceptions.ConnectionError as e:
        reports = [{
            'date_from': 'Нет возможности соединиться с сервером запросов',
            'date_to': '',
            'status': f'{e}',
        }]

    return render_template('history.html', reports=reports, user=current_user, URL=URL_TO_API)


@profile_blueprint.after_request
def redirect_to_sing_in(response):
    if response.status_code == 401:
        return redirect(url_for('login_blueprint.login_page') + '?next=' + request.url)

    return response
