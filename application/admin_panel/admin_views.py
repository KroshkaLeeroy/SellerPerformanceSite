import requests
from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from application.config import URL_TO_API, ADMIN_KEY
from application.models import Payments
from application.setup import User, db, Requests, Keys
from application.utils import check_reports_from_API, check_reports_from_API_dev_log, generate_password

admin_blueprint = Blueprint('admin_blueprint', __name__)


@admin_blueprint.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_page():
    if current_user.account_type != 'admin':
        return redirect('/profile')

    if request.method == 'POST':
        name = request.form.get('search')
        users = User.query.filter(User.email.like(f"%{name}%")).all()
        user_ids = User.query(User.id).filter(User.email.like(f"%{name}%")).all()
        reqs = Requests.query.filter(Requests.parent_id.in_(user_ids)).all()

    else:
        users = User.query.all()
        reqs = Requests.query.all()
    return render_template('admin_panel_list.html', user=current_user, users=users, reqs=reqs)


@admin_blueprint.route('/admin_panel/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_page_user(user_id):
    if current_user.account_type != 'admin':
        return redirect('/profile')

    user = User.query.get(user_id)
    keys = Keys.query.get(user_id)
    req = Requests.query.get(user_id)

    if request.method == 'POST':

        date = request.form.get('date-query')
        email = request.form.get('email')
        api_seller = request.form.get('api_seller')
        client_id_seller = request.form.get('client_id_seller')
        api_performance = request.form.get('api_performance')
        client_id_performance = request.form.get('client_id_performance')
        account_type = request.form.get('account_type')
        request_count = request.form.get('request_count')

        if date:
            # TODO: Запрос к API приложения с историей запросов по дате
            pass

        if email:
            user.email = email
        if api_seller:
            keys.api_key_seller = api_seller
        if client_id_seller:
            keys.client_id_seller = client_id_seller
        if api_performance:
            keys.api_key_performance = api_performance
        if client_id_performance:
            keys.client_id_performance = client_id_performance
        if account_type:
            user.account_type = account_type
        if request_count:
            req.request_count = request_count
        db.session.commit()

    try:
        reports = check_reports_from_API(URL_TO_API, keys.client_id_seller)
    except requests.exceptions.ConnectionError as e:
        reports = [{
            'time_from': 'Нет возможности соединиться с сервером запросов',
            'time_to': '',
            'status': f'{e}',
        }]
    return render_template('admin_panel_user.html', user=current_user, user_1=user, req=req, keys=keys,
                           reports=reports, URL=URL_TO_API)


@admin_blueprint.route('/admin_panel/<int:user_id>/delete/action=<action>', methods=['GET', 'POST'])
@login_required
def admin_page_user_delete(user_id, action):
    if current_user.account_type != 'admin':
        return redirect('/profile')

    user = User.query.get(user_id)

    if action == 'restore':
        user.is_account_active = True
        db.session.commit()
        return redirect(url_for('admin_blueprint.admin_page'))
    elif action == 'delete-unreturned':
        reqs = Requests.query.filter_by(parent_id=user_id).all()
        for req in reqs:
            db.session.delete(req)
        keys = Keys.query.filter_by(parent_id=user_id).all()
        for key in keys:
            db.session.delete(key)
        payments = Payments.query.filter_by(parent_id=user_id).all()
        for payment in payments:
            db.session.delete(payment)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin_blueprint.admin_page'))
    elif action == 'delete':
        user.is_account_active = False
        db.session.commit()
    return redirect(url_for('admin_blueprint.admin_page'))


@admin_blueprint.route('/report_log/<user_id>/<report_data>', methods=['GET', 'POST'])
@login_required
def report_log(user_id, report_data):
    if current_user.account_type != 'admin':
        return redirect('/profile')
    data = check_reports_from_API_dev_log(URL_TO_API, ADMIN_KEY, user_id, report_data)

    if data.status_code == 200:
        try:
            data = data.json()
            return render_template('admin_log_reports_reader.html',
                                   data=data,
                                   user_id=user_id,
                                   report_data=report_data,
                                   admin_key=ADMIN_KEY,
                                   url_to_API=URL_TO_API, )
        except Exception as e:
            return jsonify({'error': f'error {e}'}), 400
    return jsonify({'error': f'report log not found {data.text}'}), 400


@admin_blueprint.route('/admin_panel/add-new-users', methods=['GET', 'POST'])
@login_required
def add_new_users():
    if current_user.account_type != 'admin':
        return redirect('/profile')
    if request.method == 'POST':
        users_list = request.form.get('data_list')
        already_exist = []
        registered = []
        for user in users_list.split('\n'):
            if not user or user.isspace() or '' == user or '@' not in user:
                continue
            email = user
            password = generate_password(10)
            if User.query.filter_by(email=email).first():
                already_exist.append(email)
                continue
            hash_pwd = generate_password_hash(password)
            user = User(password=hash_pwd, account_type='user', email=email)
            key = Keys(parent_id=user.id)
            req = Requests(parent_id=user.id)
            pay = Payments(parent_id=user.id)

            db.session.add(key)
            db.session.add(req)
            db.session.add(pay)

            db.session.add(user)
            db.session.commit()

            registered.append({'email': email, 'password': password})

        return render_template('admin_panel_add_new_users.html', already_exist=already_exist,
                               registered=registered)

    return render_template('admin_panel_add_new_users.html', user=current_user)


@admin_blueprint.route('/admin_panel/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_page_user_edit(user_id):
    if current_user.account_type != 'admin':
        return redirect(url_for('profile_blueprint.profile_page'))

    user = User.query.get(user_id)
    req = Requests.query.get(user_id)
    keys = Keys.query.get(user_id)

    return render_template('admin_panel_user_edit.html', user=current_user, req=req, keys=keys, user_1=user)
