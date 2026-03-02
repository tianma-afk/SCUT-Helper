from dotenv import load_dotenv
import os
# 加载 .env 文件
load_dotenv()
# -------------------------- 数据库配置 --------------------------
ASYNC_DATABASE_URL = (
    f"mysql+aiomysql://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
    f"?charset={os.getenv('DB_CHARSET', 'utf8mb4')}"
)

# -------------------------- 邮件发送配置 --------------------------
# 示例：QQ邮箱配置（需开启SMTP并获取授权码）
SMTP_HOST = os.getenv("SMTP_HOST")       # SMTP服务器地址
SMTP_PORT = int(os.getenv("SMTP_PORT"))  # SMTP端口（SSL加密）
SMTP_USER = os.getenv("SMTP_USER") # 发件人邮箱
SMTP_PASS = os.getenv("SMTP_PASS")    # 邮箱SMTP授权码（非登录密码）
SENDER_NAME = os.getenv("SENDER_NAME")     # 发件人显示名称


# -------------------------- JWT配置 --------------------------
from passlib.context import CryptContext
# 密码加密上下文（BCrypt算法）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# JWT配置（需和项目统一）
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24*7  # Token有效期1周

# -------------------------- HTTPS配置 --------------------------
SSL_KEYFILE = os.getenv("SSL_KEYFILE")
SSL_CERTFILE = os.getenv("SSL_CERTFILE")
PORT = int(os.getenv("PORT"))

# -------------------------- 密码校验配置 --------------------------
import re
# 密码校验正则（至少8位，包含字母和数字）
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$')