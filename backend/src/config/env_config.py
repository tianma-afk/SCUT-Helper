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

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"


    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    SENDER_NAME: str

    JWT_SECRET_KEY: str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

    SSL_KEYFILE: str
    SSL_CERTFILE: str
    PORT: int = 8443

    API_KEY: str

    model_config = {"env_file": "config/.env", "env_file_encoding": "utf-8"}


settings = Settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$')

