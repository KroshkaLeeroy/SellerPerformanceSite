import time
from logging import info

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from .subscriptions import update_user_subscription
from .yookassa_api import PData, Payment, check_payments
from ..models import Payments, Requests

payment_blueprint = Blueprint('payment_blueprint', __name__)


@payment_blueprint.route('/payment', methods=['GET', 'POST'])
@login_required
def payment_page():
    requests = Requests.query.get(current_user.id).request_count
    payments = Payments.query.get(current_user.id)
    shops_count_max = 10

    if request.method == 'POST':
        plan = float(request.form.get("plan-type"))
        months = int(request.form.get("months"))
        shops = int(request.form.get("shops"))
        autopay = bool(request.form.get("autopays"))

        plan_name = "Базовый" if plan == 4990 else "Старт"
        autopay_label = "подключено" if autopay else "не подключено"

        total = plan * months
        if shops > 1:
            total += (shops - 1) * 2990
        if months == 12:
            total *= 0.75
        elif months >= 6:
            total *= 0.85

        payment_data = PData(total, return_url=url_for("payment_blueprint.after_payment"),
                             description=f"[Пользователь {current_user.id}]: Покупка плана '{plan_name}' на {shops} "
                                         f"магазинов и {months} месяцев. Автопродление {autopay_label}.")
        payment = Payment(payment_data.get_data())
        info(payment_data.get_data())
        if payment.validate_data():
            redir = payment.pay()
            return redirect(redir)
        else:
            flash("Something went wrong.", "warning")
    if payments.plan == 'start':
        payments.plan = "Старт"
    elif payments.plan == 'basic':
        payments.plan = "Базовый"
    else:
        payments.plan = "Пробный"  # trial

    if payments.autopay:
        payments.autopay = "Включено"
    else:
        payments.autopay = "Не подключено"

    payments.payment_date = str(payments.payment_date.date()).replace('-', '.')

    return render_template('payments.html', user=current_user, payments=payments, requests=requests,
                           scm=shops_count_max)


@payment_blueprint.route('/after_payment')
@login_required
def after_payment():
    pays = check_payments()
    for id0 in pays:
        payment = Payment(PData(0)).find_one(id0)
        if payment["status"] == "succeeded" and payment["paid"] == True:
            data = payment.description.replace('[Пользователь ', '').replace(']: Покупка плана \'', ' ').replace('\' на', '')\
                .replace(' магазинов и', '').replace('месяцев. Автопродление ', '').replace('.', '').split(' ')
            print(data)
            update_user_subscription(int(data[0]), True, data[1], int(data[2]), int(data[3]), data[4])
    return redirect(url_for("payment_blueprint.payment_page"))


@payment_blueprint.after_request
def redirect_to_sign_in(response):
    if response.status_code == 401:
        return redirect(url_for('login_blueprint.login_page') + '?next=' + request.url)
    return response
