# router/users.py
from crud.user_login_log import create_login_log
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import create_user, get_user_by_account, verify_password, get_all_users
from crud.user_security import init_user_security, increment_login_attempts, get_user_security ,reset_security_status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db_config import get_db
from pydantic import Field

# -------------------------- 定义接口请求/响应模型 --------------------------
router = APIRouter(prefix="/api/users", tags=["用户管理"])  # 接口前缀/api/users，标签分类

# 注册请求体
class RegisterRequest(BaseModel):
    username: str=Field(...,description="用户名",min_length=1,max_length=50)
    account_name: str=Field(...,description="账户名",min_length=1,max_length=20)
    password: str=Field(...,description="密码",min_length=1,max_length=255)

# 登录请求体
class LoginRequest(BaseModel):
    account_name: str=Field(...,description="账户名",min_length=1,max_length=20)
    password: str=Field(...,description="密码",min_length=1,max_length=255)
    ip_address: str=Field(...,description="登录IP地址",min_length=1,max_length=50)

# -------------------------- 注册接口 --------------------------
@router.post("/register",summary="用户注册",description="用户注册接口，注册新用户")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """用户注册接口"""
    # 1. 先检查账户是否已存在
    existing_user = await get_user_by_account(db, request.account_name)
    if existing_user:
        raise HTTPException(status_code=400, detail="账户名已存在")
    
    # 2. 创建用户
    new_user = await create_user(
        db=db,
        username=request.username,
        account_name=request.account_name,  # 账户名唯一
        password=request.password
    )
    
    if not new_user:
        raise HTTPException(status_code=500, detail="注册失败")
    
    # 2. 初始化安全记录
    await init_user_security(db, new_user.user_id)

    # 3. 返回用户信息（隐藏密码哈希）
    return {
        "success": True,
        "message": "注册成功",
        "data": {
            "user_id": new_user.user_id,
            "username": new_user.username,
            "account_name": new_user.account_name
        }
    }

# -------------------------- 登录接口 --------------------------
@router.post("/login",summary="用户登录",description="用户登录接口，登录已注册用户")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """用户登录接口"""
    # 1. 根据账户名查询用户
    user = await get_user_by_account(db, request.account_name)
    if not user:
        # 不暴露“账户不存在”，统一提示“账户名或密码错误”，提升安全性
        raise HTTPException(status_code=401, detail="账户名或密码错误")
    
    # 2. 验证账户是否被锁定
    user_security = await get_user_security(db, user.user_id)
    if user_security.is_locked:
        # 登录失败，记录日志
        await create_login_log(
            db=db,
            user_id=user.user_id,
            ip_address=request.ip_address,
            success=False
        )
        raise HTTPException(status_code=403, detail="账户已被锁定") 
        

    # 3. 验证密码
    if not verify_password(request.password, user.password_hash):
        await increment_login_attempts(db, user.user_id)
        # 登录失败，记录日志
        await create_login_log(
            db=db,
            user_id=user.user_id,
            ip_address=request.ip_address,
            success=False
        )
        raise HTTPException(status_code=401, detail="账户名或密码错误")
    
    # 4. 登录成功，记录日志
    await create_login_log(
        db=db,
        user_id=user.user_id,
        ip_address=request.ip_address,  
        success=True
    )


    # 5. 登录成功，重置登录尝试次数
    await reset_security_status(db, user.user_id)


    # 6. 登录成功（后续可扩展生成token）
    return {
        "success": True,
        "message": "登录成功",
        "data": {
            "user_id": user.user_id,
            "username": user.username,
            "account_name": user.account_name
        }
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
                "account_name": user.account_name
            }
            for user in users
        ]
    }