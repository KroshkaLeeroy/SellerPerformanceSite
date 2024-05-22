import requests
from sqlalchemy import create_engine, text
from application.init import app, db, User, Keys, Requests, Payments


def check_reports_from_API(URL, user_id):
    existing_reports = requests.get(f'{URL}/check-pull/{user_id}')
    if existing_reports.status_code == 200:
        reports = existing_reports.json()
        reports = reports.get('history')
        if reports:
            reports = reports[::-1]
        else:
            reports = [{
                'date_from': 'Не удалось перевернуть отчеты',
                'date_to': '',
                'status': f'',
            }]
    else:
        reports = [{
                'date_from': 'Ненормальный ответ сервера',
                'date_to': f'{existing_reports.text}',
                'status': f'{existing_reports.status_code}',
            }]
    return reports


def migrate_database():
    old_database_engine = create_engine("sqlite:///instance/old_main_db.db")
    with old_database_engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM user_table"))
        with app.app_context():
            for row in result:
                if row[2] != "admin@mail.ru":
                    user = User(password=row[1], email=row[2], account_type=row[7])
                    db.session.add(user)
                    db.session.commit()
                    key = Keys(parent_id=user.id, api_key_seller=row[3], client_id_seller=row[4],
                               api_key_performance=row[5],
                               client_id_performance=row[6])
                    request = Requests(parent_id=user.id, request_count=row[8])
                    payment = Payments(parent_id=user.id)
                    db.session.add(key)
                    db.session.add(request)
                    db.session.add(payment)
                    db.session.commit()
