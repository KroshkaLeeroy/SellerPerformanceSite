from datetime import datetime as dt, timedelta as td
from logging import debug, info

from application.init import app
from application.models import db, User, Payments


def payment_polling():
    cur_date = dt.now()
    debug('[' + str(cur_date) + ']: ' + 'payment checking procedure launched!')
    with app.app_context():
        users = User().query.all()
        for user in users:
            if user.account_type == "admin":
                continue
            payday = Payments().query.get(user.id)
            if payday.payment_date is None:
                db.session.query(Payments).filter(Payments.parent_id == user.id).update({"payment_date": dt.now()})
                payday = Payments().query.get(user.id)
                db.session.commit()
            diff = (cur_date - payday.payment_date)
            if payday.plan == "trial":
                if diff.days > 3:
                    if payday.autopay:
                        if pay_by_autopay():
                            info('[' +
                                 str(dt.now()) + f']: user\'s plan with id={user.id} ({user.email}) was paid!')
                        else:
                            info('[' +
                                 str(dt.now()) + f']: user\'s plan with id={user.id} ({user.email}) was deactivated '
                                                 f'due to failed payment')
                            payday.is_plan_active = False
                    else:
                        payday.is_plan_active = False
            else:
                if diff.days > 0:
                    if payday.autopay:
                        if pay_by_autopay():
                            info('[' +
                                 str(dt.now()) + f']: user\'s plan with id={user.id} ({user.email}) was paid!')
                        else:
                            info('[' +
                                 str(dt.now()) + f']: user\'s plan with id={user.id} ({user.email}) was deactivated '
                                                 f'due to failed payment')
                            payday.is_plan_active = False
                    else:
                        payday.is_plan_active = False


def pay_by_autopay() -> bool:
    return False


def update_user_subscription(user_id: int, is_active: bool = False, plan: str = "", shops: int = 1, months: int = 1,
                             autopay: bool = False):
    print(user_id, is_active, plan, shops, months, autopay)
    print(type(months))
    if plan == 'Старт':
        plan = 'start'
    elif plan == 'Базовый':
        plan = 'basic'
    else:
        plan = 'trial'

    if autopay == 'подключено':
        autopay = True
    else:
        autopay = False
    with (app.app_context()):
        pay = Payments.query.get(user_id)

        pay.is_plan_active = True
        pay.plan = plan
        pay.shops_connected = shops
        pay.payment_date = (dt.now() + td(days=months * 30))
        pay.autopay = autopay
        db.session.commit()
