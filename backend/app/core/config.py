"""
作用：配置项目，包括项目名称、API前缀和数据库路径等。
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
# 计算项目根路径（backend的父目录）
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # 指向scut_helper

class Settings(BaseSettings):
    PROJECT_NAME: str = "鲤工助手"
    API_V1_STR: str = "/api/v1"
    
    # 数据库路径：相对于项目根目录
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/assistant.db"
    
    # 从backend/.env加载配置
    model_config = ConfigDict(env_file=os.path.join(BASE_DIR, "backend", ".env"))

settings = Settings()
print(BASE_DIR)