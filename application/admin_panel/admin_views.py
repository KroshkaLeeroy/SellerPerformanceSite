from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from flask_login import current_user, login_required
from application.setup import User, db
from application.config import URL_TO_API
from application.utils import check_reports_from_API
import requests

admin_blueprint = Blueprint('admin_blueprint', __name__)


@admin_blueprint.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_page():
    if current_user.account_type != 'admin':
        return redirect('/profile')

    if request.method == 'POST':
        name = request.form.get('search')
        users = User.query.filter(User.email.like(f"%{name}%")).all()

    else:
        users = User.query.all()
    return render_template('admin_panel_list.html', user=current_user, users=users)


@admin_blueprint.route('/admin_panel/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_page_user(user_id):
    if current_user.account_type != 'admin':
        return redirect('/profile')

    user = User.query.get(user_id)

    if request.method == 'POST':

        date = request.form.get('date-query')
        email = request.form.get('email')
        api_seller = request.form.get('api_seller')
        client_id_seller = request.form.get('client_id_seller')
        api_performance = request.form.get('api_performance')
        account_type = request.form.get('account_type')
        request_count = request.form.get('request_count')
        client_id_performance = request.form.get('client_id_performance')

        if date:
            # TODO: Запрос к API приложения с историей запросов по дате
            pass

        if email:
            user.email = email
        if api_seller:
            user.api_key_seller = api_seller
        if api_performance:
            user.api_key_performance = api_performance
        if account_type:
            user.account_type = account_type
        if request_count:
            user.request_count = request_count
        if client_id_seller:
            user.client_id_seller = client_id_seller
        if client_id_performance:
            user.client_id_performance = client_id_performance

        db.session.commit()

    try:
        reports = check_reports_from_API(URL_TO_API, user.client_id_seller)
    except requests.exceptions.ConnectionError as e:
        reports = [{
            'date_from': 'Нет возможности соединиться с сервером запросов',
            'date_to': '',
            'status': f'{e}',
        }]

    return render_template('admin_panel_user.html', user=current_user, user_1=user, history_records=reports,
                           URL=URL_TO_API)


@admin_blueprint.route('/admin_panel/<int:user_id>/delete/action=<action>', methods=['GET', 'POST'])
@login_required
def admin_page_user_delete(user_id, action):
    if current_user.account_type != 'admin':
        return redirect('/profile')

    user = User.query.get(user_id)

    if action == 'restore':
        user.account_status = 'active'
        db.session.commit()
        return redirect(url_for('admin_blueprint.admin_page'))
    else:
        user.account_status = 'deleted'
        db.session.commit()
    return redirect(url_for('admin_blueprint.admin_page'))


@admin_blueprint.route('/report_log/<user_id>/<report_data>', methods=['GET', 'POST'])
@login_required
def report_log(user_id, report_data):
    if current_user.account_type != 'admin':
        return redirect('/profile')
    url = f'{URL_TO_API}/MraK1911_!@#/{user_id}/{report_data}'
    data = requests.get(url)
    print(data, url)
    if data.status_code == 200:
        return jsonify(data.text)
    return jsonify({'error': f'report log not found {data.text}'}), 400


@admin_blueprint.route('/admin_panel/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_page_user_edit(user_id):
    if current_user.account_type != 'admin':
        return redirect(url_for('profile_blueprint.profile_page'))

    user = User.query.get(user_id)
    return render_template('admin_panel_user_edit.html', user=current_user, user_1=user)
