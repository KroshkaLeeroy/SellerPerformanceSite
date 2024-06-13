import requests


def check_reports_from_API(URL, user_id):
    URL = f'{URL}/check-pull/{user_id}'
    print(URL)
    existing_reports = requests.get(URL, verify=False)
    if existing_reports.status_code == 200:
        reports = existing_reports.json()
        reports = reports.get('history')
        if reports:
            reports = reports[::-1]
        else:
            reports = [{
                'time_from': 'Не удалось перевернуть отчеты',
                'time_to': '',
                'status': f'',
            }]
    else:
        reports = [{
                'time_from': 'Ненормальный ответ сервера',
                'time_to': f'',
                'status': f'{existing_reports.status_code}',
            }]
    return reports
