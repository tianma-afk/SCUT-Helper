from pydantic_settings import BaseSettings
from passlib.context import CryptContext
import re


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_CHARSET: str = "utf8mb4"

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    SENDER_NAME: str

    JWT_SECRET_KEY: str

    SSL_KEYFILE: str
    SSL_CERTFILE: str
    PORT: int = 8443

    model_config = {"env_file": "config/.env", "env_file_encoding": "utf-8"}


settings = Settings()

ASYNC_DATABASE_URL = (
    f"mysql+aiomysql://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}"
    f"/{settings.DB_NAME}"
    f"?charset={settings.DB_CHARSET}"
)

SMTP_HOST = settings.SMTP_HOST
SMTP_PORT = settings.SMTP_PORT
SMTP_USER = settings.SMTP_USER
SMTP_PASS = settings.SMTP_PASS
SENDER_NAME = settings.SENDER_NAME

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24 * 7

SSL_KEYFILE = settings.SSL_KEYFILE
SSL_CERTFILE = settings.SSL_CERTFILE
PORT = settings.PORT

PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$')
