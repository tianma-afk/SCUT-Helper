from routers import user_security
from routers import users
from routers import user_login_log
from routers import products
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.env_config import SSL_KEYFILE, SSL_CERTFILE, PORT
from fastapi import APIRouter

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中请指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(users.router)
main_router.include_router(user_security.router)
main_router.include_router(user_login_log.router)
main_router.include_router(products.router)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, ssl_keyfile=SSL_KEYFILE, ssl_certfile=SSL_CERTFILE)
# 在app路径下启动虚拟环境的命令：..\venv\Scripts\activate.bat
# 运行命令：python main.py
# 访问FastAPI的交互式接口文档：https://127.0.0.1:8443/docs

