import requests


def check_reports_from_API(URL, user_id):
    existing_reports = requests.get(f'{URL}/check-pull/{user_id}')
    if existing_reports.status_code == 200:
        reports = existing_reports.json()
        reports = reports.get('history')
        if reports:
            reports = reports[::-1]
        else:
            reports = []
    else:
        reports = []
    return reports
