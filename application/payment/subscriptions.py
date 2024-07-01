from datetime import datetime as dt, timedelta as td
from logging import debug, info
from .yookassa_api import pay_by_autopay
from application.init import app
from application.models import db, User, Payments


def payment_polling():
    cur_date = dt.now()
    debug(f'[{cur_date}]: payment checking procedure launched!')
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.account_type == "admin":
                continue
            payday = Payments.query.get(user.id)
            if not payday.payment_date:
                db.session.query(Payments).filter(Payments.parent_id == user.id).update({"payment_date": dt.now()})
                payday = Payments.query.get(user.id)
                db.session.commit()
            check_and_update_payment_status(user, payday, cur_date)


def check_and_update_payment_status(user, payday, cur_date):
    diff = (cur_date - payday.payment_date).days
    plan_expired = (payday.plan == "trial" and diff > 3) or (payday.plan != "trial" and diff > 0)

    if plan_expired:
        if payday.autopay:
            if pay_by_autopay():
                info(f'[{dt.now()}]: user\'s plan with id={user.id} ({user.email}) was paid!')
            else:
                info(
                    f'[{dt.now()}]: user\'s plan with id={user.id} ({user.email}) was deactivated due to failed payment')
                payday.is_plan_active = False
        else:
            payday.is_plan_active = False
        db.session.commit()


def update_user_subscription(user_id: int, is_active: bool = False, pay_plan: str = "", shops: int = 1, months: int = 1,
                             autopay: bool = False):
    info(user_id, is_active, pay_plan, shops, months, autopay)
    info(type(months))
    plan_dict = {
        'Старт': 'start',
        'Базовый': 'basic',
    }

    if pay_plan in plan_dict:
        bd_plan = plan_dict[pay_plan]
    else:
        bd_plan = 'trial'

    autopay = (autopay == 'подключено')

    with app.app_context():
        pay = Payments.query.get(user_id)
        pay.is_plan_active = is_active
        pay.plan = bd_plan
        pay.shops_connected = shops
        pay.payment_date = dt.now() + td(days=months * 30)
        pay.autopay = autopay
        db.session.commit()
