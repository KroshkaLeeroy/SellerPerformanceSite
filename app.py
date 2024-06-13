import os
from datetime import datetime

from flask_apscheduler import APScheduler
from werkzeug.security import generate_password_hash

from application.config import ADMIN_PASSWORD
from application.init import app, db, User, Keys, Requests, Payments
from application.payment.subscriptions import payment_polling
from application.payment.yookassa_api import after_payment
import urllib3

urllib3.disable_warnings()

with app.app_context():
    db.create_all()
    user = User.query.filter_by(email='admin@mail.ru').first()
    if not user:
        hash_pwd = generate_password_hash(ADMIN_PASSWORD)
        user = User(password=hash_pwd, account_type='admin', email='admin@mail.ru')
        db.session.add(user)
        db.session.commit()
        keys = Keys(parent_id=(user.id))
        payments = Payments(parent_id=(user.id), plan="trial", autopay=False, shops_connected=0,
                            payment_date=datetime(2024, 4, 23))
        requests = Requests(parent_id=(user.id), request_count=0)
        db.session.add(keys)
        db.session.add(payments)
        db.session.add(requests)
        db.session.commit()

def schedule_jobs():
    scheduler = APScheduler()
    app.debug = True if app.debug =="True" else False
    if not app.debug:
        scheduler.add_job(id='check_payments', func=payment_polling, trigger='cron', hour=12, minute=0, second=0)
        scheduler.add_job(id='check_billing', func=after_payment, trigger='interval', seconds=60)
        scheduler.start()

# schedule_jobs()
if __name__ == '__main__':
    app.run(debug=False)
