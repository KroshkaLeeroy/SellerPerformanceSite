from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import requests

from application.setup import db, User, Keys, Requests, Payments

login_blueprint = Blueprint('login_blueprint', __name__, template_folder='templates')


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')

    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.main_page'))

    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):

            next_page = request.args.get('next')

            if not user.is_account_active:
                flash('Ваш аккаунт был удалён или заблокирован')
                return redirect(url_for('login_blueprint.login_page'))
            else:
                login_user(user)
                return redirect(next_page if next_page else url_for('main_blueprint.main_page'))
        else:
            flash('Логин или пароль неверны')
    else:
        if request.method == 'POST':
            flash('Пожалуйста, заполните все поля')
    return render_template('login.html', user=current_user)


@login_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@login_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile_blueprint.profile_page'))

    return redirect(url_for('login_blueprint.not_ready'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        policy = request.form.get('accept-policy')

        # TODO добавить страницы с условиями и Политикой конфиденциальности

        if not (email or password or password2):
            flash('Пожалуйста, заполните все поля')
        elif not policy:
            flash('Необходимо согласиться с Условиями и Политикой Конфиденциальности')
        elif password != password2:
            flash('Пароли не совпадают')
        elif email and User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже зарегистрирован')
            return redirect(url_for('login_blueprint.login_page'))
        else:
            hash_pwd = generate_password_hash(password)
            user = User(password=hash_pwd, account_type='user', email=email)
            db.session.add(user)

            key = Keys(parent_id=user.id)
            req = Requests(parent_id=user.id)
            pay = Payments(parent_id=user.id)

            db.session.add(key)
            db.session.add(req)
            db.session.add(pay)
            db.session.commit()

            return redirect(url_for('login_blueprint.login_page'))

    return render_template('register.html', user=current_user)


@login_blueprint.route('/not-ready')
def not_ready():
    return render_template('not_ready.html')

@login_blueprint.after_request
def redirect_to_sing_in(response):
    if response.status_code == 401:
        return redirect(url_for('login_blueprint.login_page') + '?next=' + request.url)

    return response
