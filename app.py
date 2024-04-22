from application.init import app, db, User, Keys, Requests, Payments
from werkzeug.security import generate_password_hash
from application.config import ADMIN_PASSWORD


with app.app_context():
    db.create_all()
    user = User.query.filter_by(email='admin').first()
    if not user:
        hash_pwd = generate_password_hash(ADMIN_PASSWORD)
        user = User(password=hash_pwd, account_type='admin', email='admin')
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=False, port='9999')
