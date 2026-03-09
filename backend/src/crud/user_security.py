from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.user_security import UserSecurity
from datetime import datetime, timedelta

# -------------------------- 初始化相关 --------------------------
async def init_user_security(db: AsyncSession, user_id: str):
    """
    新用户注册时，初始化对应的安全记录
    :param db: 数据库会话
    :param user_id: 新用户的UUID
    :return: 新建的安全记录对象
    """
    # 创建安全记录对象，默认失败次数0，未锁定
    db_security = UserSecurity(
        user_id=user_id,
        login_attempts=0,
        is_locked=False
    )
    
    # 写入数据库
    db.add(db_security)
    await db.commit()
    await db.refresh(db_security)
    return db_security

# -------------------------- 查询相关 --------------------------
async def get_user_security(db: AsyncSession, user_id: str):
    """
    根据 user_id 查询用户的安全记录
    :param db: 数据库会话
    :param user_id: 用户UUID
    :return: 安全记录对象 / None
    """
    result = await db.execute(select(UserSecurity).where(UserSecurity.user_id == user_id))
    return result.scalars().first()

# -------------------------- 更新相关 --------------------------
async def increment_login_attempts(db: AsyncSession, user_id: str, max_attempts: int = 5):
    """
    登录失败时，增加失败次数，并判断是否需要锁定账户
    :param db: 数据库会话
    :param user_id: 用户UUID
    :param max_attempts: 最大允许失败次数，默认5次
    :return: 更新后的安全记录对象
    """
    # 1. 查询当前记录
    security = await get_user_security(db, user_id)
    if not security:
        return None
    
    # 2. 失败次数 +1
    security.login_attempts += 1
    
    # 3. 判断是否达到锁定阈值
    if security.login_attempts >= max_attempts:
        security.is_locked = True

    # 4. 提交更新
    await db.commit()
    await db.refresh(security)
    return security

async def reset_security_status(db: AsyncSession, user_id: str):
    """
    登录成功时，重置失败次数并解锁账户
    :param db: 数据库会话
    :param user_id: 用户UUID
    :return: 更新后的安全记录对象
    """
    # 1. 查询当前记录
    security = await get_user_security(db, user_id)
    if not security:
        return None
    
    # 2. 重置状态
    security.login_attempts = 0
    security.is_locked = False

    # 3. 提交更新
    await db.commit()
    await db.refresh(security)
    return security

async def unlock_user_manual(db: AsyncSession, user_id: str):
    """
    管理员手动解锁账户
    :param db: 数据库会话
    :param user_id: 用户UUID
    :return: 更新后的安全记录对象
    """
    # 1. 锁定状态设为False
    await db.execute(
        update(UserSecurity)
        .where(UserSecurity.user_id == user_id)
        .values(login_attempts=0, is_locked=False)
    )
    await db.commit()
    
    # 返回更新后的对象
    return await get_user_security(db, user_id)