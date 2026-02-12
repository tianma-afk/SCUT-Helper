from sqlalchemy import String, CHAR, SMALLINT, BOOLEAN, DATETIME
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from .base import Base  
import uuid


class User(Base):
    __tablename__ = "users"  # 对应数据库中的users表

    # 主键：用户UUID
    user_id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        comment='用户UUID，主键',
        default=uuid.uuid4,  # 自动生成UUID
        index=True
    )
    
    # 核心登录字段：用户邮箱（唯一）
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment='用户邮箱（核心登录标识），唯一不可重复',
        index=True  # 对应数据表的idx_email索引
    )
    
    # 密码哈希值（可选，为空则仅支持验证码登录）
    password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment='密码哈希值（BCrypt加密存储），为空则仅支持验证码登录'
    )
    
    # 用户名
    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment='用户名'
    )
    
    # 用户头像URL（可选）
    headimg_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment='用户头像URL（可选）'
    )
    
    # 性别：0未知，1男，2女（默认0）
    gender: Mapped[int] = mapped_column(
        SMALLINT,
        nullable=False,
        default=0,
        comment='性别：0未知，1男，2女'
    )
    

    def __repr__(self) -> str:
        """模型的字符串表示，便于调试"""
        return (
            f"User(user_id={self.user_id!r}, email={self.email!r}, "
            f"username={self.username!r}, gender={self.gender!r})"
        )