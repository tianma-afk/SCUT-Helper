from fastapi import FastAPI
from routers import products
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    #允许的源，*表示允许所有
    allow_credentials=True, #允许携带cookie
    allow_methods=["*"],    #允许的请求⽅法
    allow_headers=["*"],    #允许的请求头
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(products.router)