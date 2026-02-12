from fastapi import FastAPI
import uvicorn
import ssl
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "HTTPS is working!"}

if __name__ == "__main__":
    # 核心：添加ssl_keyfile和ssl_certfile参数
    uvicorn.run(
        "test:app",  # 你的主文件名称:app实例
        host="0.0.0.0",  # 允许外部访问
        port=443,  # HTTPS默认端口
        ssl_keyfile="./key.pem",  # 私钥文件路径
        ssl_certfile="./cert.pem"  # 证书文件路径
    )