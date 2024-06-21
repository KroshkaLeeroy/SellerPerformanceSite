import json
import os
import random
from base64 import urlsafe_b64encode
from string import printable

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from application.config import ENCRYPTING_PASSWORD


def generate_password(length):
    return ''.join(random.choice(printable) for _ in range(length))


def normalize_date(date: str) -> str:
    if len(date) == 16:
        date = f"{date[8:11]}.{date[5:7]}.{date[:4]} {date[-5:-3]}:{date[-2:]}"
    elif len(date) == 10:
        date = f"{date[8:11]}.{date[5:7]}.{date[:4]}"
    return date


def check_reports_from_API(url, user_id):
    enc_user_id = encrypt_data(ENCRYPTING_PASSWORD, user_id)
    url = f'{url}/check-pull/{enc_user_id}'
    existing_reports = requests.get(url, verify=False)
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
            'time_from': f'{existing_reports.status_code}',
            'time_to': f'',
            'status': f'',
        }]

    for report in reports:
        if 'time_created' in report.keys():
            report['time_created'] = normalize_date(report['time_created'])
        report['time_from'] = normalize_date(report['time_from'])
        report['time_to'] = normalize_date(report['time_to'])
    return reports


def check_reports_from_API_dev_log(url_to_api, admin_key, user_id, report_data):
    url = f'{url_to_api}/{admin_key}/downloads*{user_id}*{report_data}'
    data = requests.get(url, verify=False)
    return data


def post_data_to_API(url_to_api, data):
    data = encrypt_data(ENCRYPTING_PASSWORD, data)
    response = requests.post(f'{url_to_api}/add-request', json=data, verify=False)
    return response


def encrypt_data(key: bytes, data) -> str:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Проверка типа данных и сериализация
    if isinstance(data, dict):
        json_data = json.dumps(data).encode()
    elif isinstance(data, str):
        json_data = data.encode()
    else:
        raise ValueError("Data must be a dictionary or a string")

    # Добавление отступов для соответствия блочному шифру
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(json_data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_json = {
        'iv': urlsafe_b64encode(iv).decode('utf-8'),
        'data': urlsafe_b64encode(encrypted_data).decode('utf-8'),
        'type': 'json' if isinstance(data, dict) else 'string'
    }
    return json.dumps(encrypted_json)

# Генерация ключа шифрования
