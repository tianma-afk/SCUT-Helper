from typing import Dict, Optional, List
import uuid
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.users import User
from crud.email_verification_code import verify_code
from config.env_config import pwd_context, JWT_SECRET_KEY, ALGORITHM,ACCESS_TOKEN_EXPIRE_HOURS


# -------------------------- 核心CRUD函数 --------------------------
async def user_register(
    db: AsyncSession,
    email: str,
    username: str,
    password: str,
    code: str
) -> Optional[User]:
    """
    邮箱注册用户逻辑：
    1. 密码加密处理
    2. 生成UUID用户ID
    3. 创建新用户并写入数据库
    """
    try:
        # 步骤1：密码BCrypt加密
        hashed_password = pwd_context.hash(password)
        
        # 步骤2：构建用户对象
        new_user = User(
            user_id=str(uuid.uuid4()),
            email=email,
            username=username,
            password=hashed_password,
            gender=0,  # 默认未知性别
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # 步骤3：校验验证码
        ret = await verify_code(db, email, code, 2)
        if ret==False:
            raise Exception(f"验证码错误或过期")
        
        # 步骤4：写入数据库
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception:
        await db.rollback()
        return None

async def user_login(
    db: AsyncSession,
    email: str,
    password: str
) -> Optional[str]:
    """
    邮箱密码登录逻辑：
    1. 校验邮箱是否存在
    2. 校验密码是否正确
    3. 生成JWT Token返回
    """
    # 步骤1：查询用户（异步查询）
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    # 步骤2：校验密码（BCrypt验证）
    if not user or not pwd_context.verify(password, user.password):
        return None
    
    # 步骤3：生成JWT Token
    access_token = jwt.encode(
        claims={
            "user_id": user.user_id,
            "email": user.email,
            "exp": datetime.now() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        },
        key=JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )
    return access_token

async def update_user_password(
    db: AsyncSession,
    email: str,
    old_password: str,
    new_password: str
) -> bool:
    """
    修改密码逻辑：
    1. 校验原密码正确性
    2. 新密码加密处理
    3. 更新密码并提交
    """
    try:
        # 步骤1：查询用户
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        # 步骤2：校验原密码
        if not user or not pwd_context.verify(old_password, user.password):
            return False
        
        # 步骤3：新密码加密并更新
        user.password = pwd_context.hash(new_password)
        user.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(user)
        return True
    except Exception:
        await db.rollback()
        return False

async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> Optional[User]:
    """
    根据邮箱查询用户：
    用于注册时校验邮箱是否已存在
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_by_id(
    db: AsyncSession,
    user_id: str
) -> Optional[User]:
    """
    根据用户ID查询用户：
    用于登录时校验用户ID和密码
    """
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()

async def get_all_users(
    db: AsyncSession
) -> List[User]:
    """
    获取所有用户逻辑：
    异步查询所有用户并返回列表
    """
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
