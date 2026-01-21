"""
FastAPI 启动文件
"""
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def read_root():
    return {"message": "鲤工助手后端运行中"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": "conda"}