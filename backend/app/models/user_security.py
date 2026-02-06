from sqlalchemy import CHAR, INT, BOOLEAN, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from .base import Base 
import uuid

class UserSecurity(Base):
    __tablename__ = "user_security" 

    user_id: Mapped[str] = mapped_column(
        CHAR(36),
        ForeignKey("users.user_id", ondelete="CASCADE"),  # 外键关联users表，级联删除
        primary_key=True,  # 一个用户对应一条记录，user_id作为主键
        comment="关联用户UUID",
        index=True  # 建立索引，提升查询速度
    )
    login_attempts: Mapped[int] = mapped_column(
        INT,
        nullable=False,
        default=0,  # 默认失败次数为0
        comment="连续登录失败次数"
    )
    is_locked: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        default=False,  # 默认未锁定
        comment="账户锁定状态，True=锁定，False=未锁定"
    )

    def __repr__(self):
        return f"UserSecurity(user_id={self.user_id}, login_attempts={self.login_attempts}, is_locked={self.is_locked})"