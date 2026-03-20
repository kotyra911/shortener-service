import logging
from dotenv import load_dotenv
import os


load_dotenv()

lg = logging.getLogger()

# Переменные подключения к бд
class DBSettings:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')

    SQLALCHEMY_DATA_BASE_URL = (
        f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )


