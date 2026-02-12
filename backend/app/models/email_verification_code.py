from sqlalchemy import String, INTEGER, SMALLINT, DATETIME, BOOLEAN, Index
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from .base import Base  # 复用你的基础模型类


class EmailVerificationCode(Base):
    __tablename__ = "email_verification_codes"  # 对应数据库中的验证码表

    # 主键ID（自增）
    id: Mapped[int] = mapped_column(
        INTEGER,  # 对应INT UNSIGNED
        primary_key=True,
        autoincrement=True,
        comment='主键ID'
    )
    
    # 接收验证码的邮箱
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='接收验证码的邮箱'
    )
    
    # 4位数字验证码
    code: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
        comment='4位数字验证码（随机生成）'
    )
    
    # 验证码类型：1-登录，2-注册，3-找回密码
    type: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
        comment='验证码类型：1-登录，2-注册，3-找回密码'
    )
    
    # 验证码过期时间（5分钟有效期）
    expires_at: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        comment='验证码过期时间（建议5分钟有效期）'
    )
    
    # 是否已使用（防止重复验证）
    is_used: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        default=False,
        comment='是否已使用（防止重复验证）'
    )


    # 定义联合索引：email + type（匹配数据表的idx_email_type）
    __table_args__ = (
        Index("idx_email_type", "email", "type"),
    )

    def __repr__(self) -> str:
        """模型的字符串表示，便于调试"""
        return (
            f"EmailVerificationCode(id={self.id!r}, email={self.email!r}, "
            f"code={self.code!r}, type={self.type!r}, is_used={self.is_used!r})"
        )