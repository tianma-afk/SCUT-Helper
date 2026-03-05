from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt ,ExpiredSignatureError
from crud.users import get_user_by_id  
from config.db_config import get_db
from config.env_config import JWT_SECRET_KEY, ALGORITHM,ACCESS_TOKEN_EXPIRE_HOURS

# 使用 HTTPBearer 自动从 Authorization 头提取 token
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    验证 token 并返回当前用户
    这个依赖会被需要认证的接口使用
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 解码 token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录已过期，请重新登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception
    
    # 从数据库获取用户
    user = await get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    
    return user

# 可选：获取当前活跃用户（额外检查用户状态）
# async def get_current_active_user(
#     current_user = Depends(get_current_user)
# ):
#     if not current_user.is_active:  # 假设用户模型有 is_active 字段
#         raise HTTPException(status_code=400, detail="用户已被禁用")
#     return current_user