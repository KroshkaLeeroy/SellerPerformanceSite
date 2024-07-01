from logging import info

from flask import Blueprint, redirect, request, flash, render_template
from flask_login import current_user, login_required

from .yookassa_api import pay
from ..models import Payments, Requests

payment_blueprint = Blueprint('payment_blueprint', __name__)


@payment_blueprint.route('/payment', methods=['GET', 'POST'])
@login_required
def payment_page():
    requests = Requests.query.get(current_user.id).request_count
    payments = Payments.query.get(current_user.id)
    shops_count_max = 10
    if request.method == 'POST':
        try:
            plan = float(request.form.get("plan-type"))
            months = int(request.form.get("months-pick"))
            shops = int(request.form.get("shops-pick"))
            autopay = bool(request.form.get("autopays"))

            print(f"[DEBUG INFO]: plan:{plan} | months:{months} | shops:{shops} | autopay:{autopay}")

            plan_name = "Бизнес" if plan == 4990 else "Старт"
            autopay_label = "подключено" if autopay else "не подключено"

            total = plan * months
            if shops > 1:
                total += (shops - 1) * plan
            if months == 12:
                total *= 0.75
            elif months >= 6:
                total *= 0.85

            payment = pay(total, user_id=current_user.id,
                          desc_details=f"тариф {plan_name} на {months} месяцев "
                                       f"c {f'{shops - 1} дополнительными магазинами' if shops - 1 > 0 else ''}.")
            info(
                f"Пользователь {current_user.id} приобрёл тариф {plan_name}"
                f" на {months} месяцев c {f'{shops - 1} дополнительными магазинами' if shops - 1 > 0 else ''} "
                f"на сумму {total}₽")
            return redirect(payment)
        except Exception as e:
            flash(f"Ошибка при обработке платежа: {str(e)}", "danger")
    if payments.plan == 'basic':
        payments.plan = 'Бизнес'
    elif payments.plan == 'start':
        payments.plan = 'Старт'
    else:
        payments.plan = 'Пробный'
    return render_template('payments.html', user=current_user, payments=payments, requests=requests,
                           scm=shops_count_max)
