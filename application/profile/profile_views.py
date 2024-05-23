import requests
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application.config import URL_TO_API
from application.setup import db, Requests, Keys
from application.utils import check_reports_from_API

profile_blueprint = Blueprint('profile_blueprint', __name__)


@profile_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    req = Requests.query.get(current_user.id)
    keys = Keys.query.get(current_user.id)
    if request.method == 'POST':
        api_seller = request.form.get('api_seller')
        client_id_seller = request.form.get('client_id_seller')
        api_performance = request.form.get('api_performance')
        client_id_performance = request.form.get('client_id_performance')

        # mistake = True
        # if len(api_seller) != 36:
        #     flash('Seller Secret должен содержать 36 символов')
        #     mistake = False
        # if len(api_performance) != 82:
        #     flash('Performance API должен содержать 82 символа')
        #     mistake = False
        # if not client_id_seller.isdigit():
        #     flash('Client ID должен содержать только цифры')
        #     mistake = False
        # if "@advertising.performance.ozon.ru" not in client_id_performance:
        #     flash('Performance ID должен содержать @advertising.performance.ozon.ru')
        #     mistake = False
        #
        # if mistake:
        #     return render_template('edit_profile.html', user=current_user, req_c=req, keys=keys)

        current_user.email = request.form.get('email')
        keys.api_key_seller = api_seller
        keys.client_id_seller = client_id_seller
        keys.api_key_performance = api_performance
        keys.client_id_performance = client_id_performance
        db.session.commit()

    return render_template('profile.html', user=current_user, req_c=req, keys=keys)


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
            flash('Даты должны быть указаны')
        else:
            print(date_from, date_to)
            # Конвертация дат из строк в объекты datetime
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            current_date = datetime.now()

            # Проверки на порядок дат и на диапазон дат
            if date_from_obj > date_to_obj:
                flash('"Дата с" должна быть раньше "Дата по"')
                return redirect(url_for('profile_blueprint.query_page'))

            days_diff = date_to_obj - date_from_obj
            if days_diff.days > 32:
                flash('Слишком большая разница между датами, максимальный диапазон 32 дня')
                return redirect(url_for('profile_blueprint.query_page'))

            # Специфичные проверки на date_to
            yesterday = current_date - timedelta(days=1)
            thirty_two_days_ago = current_date - timedelta(days=32)
            if date_from_obj > yesterday:
                flash('"Дата с" должна быть минимум вчерашним днем')
                return redirect(url_for('profile_blueprint.query_page'))

            if date_from_obj < thirty_two_days_ago:
                flash('"Дата с" не должна быть больше 32 дней назад')
                return redirect(url_for('profile_blueprint.query_page'))

            # Отправка данных на сервер
            response = requests.post(f'{URL_TO_API}/add-request', json=data, verify=False)
            if response.status_code == 200:
                flash('Запрос успешно отправлен на сервер')
            else:
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

    if keys.api_key_seller == '' or keys.api_key_performance == '' or keys.client_id_seller == '' or keys.client_id_performance == '':
        flash(f'Заполните API ключи в Настройках профиля')

    # if len(keys.api_key_seller) != 36:
    #     flash('Seller Secret должен содержать 36 символов')
    # if len(keys.api_key_performance) != 82:
    #     print(keys.api_key_performance)
    #     flash('Performance API должен содержать 82 символа')
    # if not keys.client_id_seller.isdigit():
    #     flash('Client ID должен содержать только цифры')
    # if "@advertising.performance.ozon.ru" not in keys.client_id_performance:
    #     flash('Performance ID должен содержать @advertising.performance.ozon.ru')

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
