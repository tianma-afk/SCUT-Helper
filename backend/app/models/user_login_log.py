from sqlalchemy import BIGINT, CHAR, DATETIME, VARCHAR, BOOLEAN, ForeignKey, Index
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from .base import Base 
from datetime import datetime
class UserLoginLog(Base):
    __tablename__ = "user_login_log" 

    log_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
        comment="日志主键，自增ID"
    )
    user_id: Mapped[str] = mapped_column(
        CHAR(36),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="关联用户UUID"
    )
    login_time: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        server_default=func.now(),
        comment="登录时间"
    )
    ip_address: Mapped[str | None] = mapped_column(
        VARCHAR(45),
        comment="登录IP地址"
    )
    success: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        comment="登录是否成功：true=成功，false=失败"
    )

    # 索引：与SQL中的idx_user_login_time对应
    __table_args__ = (
        Index("idx_user_login_time", "user_id", "login_time"),
    )

    def __repr__(self):
        return f"UserLoginLog(log_id={self.log_id}, user_id={self.user_id}, success={self.success}, login_time={self.login_time})"