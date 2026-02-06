from routers import user_security
from routers import users
from routers import user_login_log
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(users.router)
app.include_router(user_security.router)
app.include_router(user_login_log.router)

# 运行命令：uvicorn main:app --reload