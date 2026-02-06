from fastapi import APIRouter
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user_login_log import UserLoginLog
from fastapi import Depends



# -------------------------- 定义接口请求/响应模型 --------------------------
router = APIRouter(prefix="/api/login_log", tags=["用户登录日志"])  # 接口前缀/api/login_log，标签分类


@router.get("/all")
async def get_all_login_logs(db: AsyncSession = Depends(get_db)):
    """
    查询所有登录日志
    :param db: 数据库会话
    :return: 登录日志列表
    """
    result = await db.execute(select(UserLoginLog))
    return result.scalars().all()
