from crud.user_login_log import create_login_log
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import get_all_users, user_register, user_login, update_user_password, get_user_by_email
from config.db_config import get_db
from pydantic import Field
import re
from crud.user_login_log import create_login_log 
from crud.email_verification_code import send_code
# -------------------------- 定义接口请求/响应模型 --------------------------
router = APIRouter(prefix="/api/users", tags=["用户管理"])  # 接口前缀/api/users，标签分类

# 密码校验正则（至少8位，包含字母和数字）
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$')

#获取验证码请求模型
class GetCodeRequest(BaseModel):
    email: EmailStr = Field(..., description="用户邮箱")

# 注册请求模型
class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="用户邮箱（登录核心标识）")
    username: str = Field(..., min_length=1, max_length=10, description="用户名，长度1-10字符")
    password: str = Field(..., min_length=8, max_length=20,description="密码，8-20位，包含字母和数字")
    code: str = Field(..., min_length=4, max_length=4, description="验证码")

# 登录请求模型（邮箱密码）
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., description="用户密码")

# 修改密码请求模型
class UpdatePasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="用户邮箱")
    old_password: str = Field(..., description="原密码")
    new_password: str = Field(..., min_length=8, description="新密码，至少8位，包含字母和数字")

#---------------------------- 获取验证码接口--------------------------
@router.post("/get_code", summary="获取验证码", description="根据邮箱获取验证码")
async def get_code(request: GetCodeRequest, db: AsyncSession = Depends(get_db)):
    # 1. 检查邮箱是否已注册
    existing_user = await get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="该邮箱已注册")
    
    # 2. 调用获取验证码逻辑
    try:
        await send_code(db, request.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "code": 200,
        "message": "验证码已发送",
    }


# -------------------------- 注册接口 --------------------------
@router.post("/register", summary="用户注册", description="邮箱注册用户，密码加密存储")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # 1. 密码格式校验
    if not PASSWORD_PATTERN.match(request.password):
        raise HTTPException(status_code=400, detail="密码格式错误：8-20位，包含字母和数字")
    
    # 2. 检查邮箱是否已注册
    existing_user = await get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="该邮箱已注册")
    
    # 3. 调用注册逻辑
    try:
        user = await user_register(
            db,
            email=request.email,
            username=request.username,
            password=request.password,
            code=request.code
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not user:
        raise HTTPException(status_code=500, detail="注册失败")
    
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "user_id": user.user_id,
            "email": user.email,
            "username": user.username
        }
    }

# -------------------------- 登录接口（邮箱密码） --------------------------
@router.post("/login", summary="用户登录", description="邮箱密码登录，返回Bearer Token")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    # 1. 调用登录逻辑（校验密码并生成token）
    token = await user_login(db, request.email, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    user = await get_user_by_email(db, request.email)
    # 2. 记录登录日志
    await create_login_log(db, user_id=user.user_id, success=True)
    
    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "access_token": token,
            "token_type": "bearer"
        }
    }

# -------------------------- 修改密码接口 --------------------------
@router.post("/update-password", summary="修改密码", description="验证原密码后修改新密码")
async def update_password(request: UpdatePasswordRequest, db: AsyncSession = Depends(get_db)):
    # 1. 新密码格式校验
    if not PASSWORD_PATTERN.match(request.new_password):
        raise HTTPException(status_code=400, detail="新密码格式错误：至少8位，包含字母和数字")
    
    # 2. 原密码与新密码不能相同
    if request.old_password == request.new_password:
        raise HTTPException(status_code=400, detail="新密码不能与原密码相同")
    
    # 3. 调用修改密码逻辑
    update_result = await update_user_password(
        db,
        email=request.email,
        old_password=request.old_password,
        new_password=request.new_password
    )
    
    if not update_result:
        raise HTTPException(status_code=400, detail="原密码错误或修改失败")
    
    return {
        "code": 200,
        "message": "密码修改成功",
        "data": None
    }

# -------------------------- 获取所有用户接口 --------------------------
@router.get("/all",summary="获取所有用户",description="获取所有用户接口，返回所有用户信息")
async def all_users(db: AsyncSession = Depends(get_db)):
    """获取所有用户接口"""
    # 1. 查询所有用户
    users = await get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="暂无用户")
    
    # 2. 返回用户列表（隐藏密码哈希）
    return {
        "success": True,
        "message": "获取所有用户成功",
        "data": [
            {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
            }
            for user in users
        ]
    }