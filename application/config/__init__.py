import os
from dotenv import load_dotenv, find_dotenv

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
