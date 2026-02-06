from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user_security import get_user_security, reset_security_status
from config.db_config import get_db
from crud.users import get_user_by_id
# -------------------------- 定义接口请求/响应模型 --------------------------
router = APIRouter(prefix="/api/security", tags=["用户安全"])  # 接口前缀/api/security，标签分类

class AdminSetSecurityRequest(BaseModel):
    user_id: str = Field(..., description="要设置的用户ID")
    login_attempts: int = Field(0, description="设置登录失败次数，默认0")
    is_locked: bool = Field(False, description="设置是否锁定，默认False（未锁定）")

@router.post("/admin/set_security_status", summary="管理员设置用户安全状态（临时接口）")
async def admin_set_security_status(
    request: AdminSetSecurityRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    管理员手动设置用户安全状态：登录失败次数、是否锁定
    （暂时不做权限校验，后续可加）
    """
    # 1. 查询用户是否存在
    user = await get_user_by_id(db, request.user_id)  # 这里用user_id查
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 2. 查询安全记录
    security = await get_user_security(db, request.user_id)
    if not security:
        raise HTTPException(status_code=404, detail="用户安全记录不存在")

    # 3. 更新安全状态
    security.login_attempts = request.login_attempts
    security.is_locked = request.is_locked

    await db.commit()
    await db.refresh(security)

    return {
        "success": True,
        "message": "用户安全状态已更新",
        "data": {
            "user_id": security.user_id,
            "login_attempts": security.login_attempts,
            "is_locked": security.is_locked
        }
    }