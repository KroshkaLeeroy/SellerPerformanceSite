import os
from yookassa import Configuration
from dotenv import load_dotenv, find_dotenv
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def generate_key(password: str, salt) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,  # 16-bytes of salt
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


if not find_dotenv():
    exit("Переменные окружение не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

DEBUG = os.getenv('DEBUG')
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SESSION_TYPE = os.getenv('SESSION_TYPE')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_DEBUG = os.getenv('MAIL_DEBUG')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
URL_TO_API = os.getenv('URL_TO_API')
ADMIN_KEY = os.getenv('ADMIN_KEY')
ENCRYPTING_KEY = os.getenv('ENCRYPTING_KEY')
SALT_KEY = os.getenv('SALT_KEY').encode()

ENCRYPTING_PASSWORD = generate_key(ENCRYPTING_KEY, SALT_KEY)

YOO_SECRET_KEY = os.getenv('YOO_SECRET_KEY')
YOO_SHOP_ID = os.getenv('YOO_SHOP_ID')

Configuration.secret_key = YOO_SECRET_KEY
Configuration.account_id = YOO_SHOP_ID
