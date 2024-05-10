from application.init import app, db, User, Keys, Requests, Payments
from werkzeug.security import generate_password_hash
from application.config import ADMIN_PASSWORD
from datetime import datetime
from application.utils import migrate_database

with app.app_context():
    db.create_all()
    user = User.query.filter_by(email='admin@mail.ru').first()
    if not user:
        hash_pwd = generate_password_hash(ADMIN_PASSWORD)
        user = User(password=hash_pwd, account_type='admin', email='admin@mail.ru')
        db.session.add(user)
        db.session.commit()
        keys = Keys(parent_id=(user.id))
        payments = Payments(parent_id=(user.id), plan="trial", autopay=False, shops_connected=0, payment_date=datetime(2024, 4, 23))
        requests = Requests(parent_id=(user.id), request_count=0)
        db.session.add(keys)
        db.session.add(payments)
        db.session.add(requests)
        db.session.commit()

if __name__ == '__main__':
    migrate_database()
    app.run(debug=False, port='9999')
