from typing import List
from datetime import datetime
from typing import Optional
from .base import Base
from sqlalchemy import DateTime, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column, relationship
from sqlalchemy import  CHAR, Index
from .users import User
class Category(Base):
    """商品分类表"""
    __tablename__ = "product_categories"
    __table_args__ = (
        Index('idx_category_name', 'category_name'), 
    )

    category_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="分类ID"
    )
    category_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="分类名称"
    )


    def __repr__(self):
        return f"<Category(category_id={self.category_id}, name={self.category_name})>"


class Product(Base):
    """商品表"""
    __tablename__ = "products"
    __table_args__ = (
        Index('idx_publisher_id', 'publisher_id'),
        Index('idx_status', 'status'),
        Index('idx_category_id', 'product_category_id'),
        Index('idx_created_at', 'created_at'),  # 按时间查询商品常用
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="商品ID"
    )
    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="商品名称"
    )
    product_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="商品价格"
    )
    product_content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="商品详细内容"
    )
    product_images: Mapped[Optional[str]] = mapped_column(
        String(2048),
        comment="商品图片URL，多个用英文逗号分隔"
    )
    trade_desc: Mapped[Optional[str]] = mapped_column(
        String(512),
        comment="商品交易描述"
    )
    
    publisher_id: Mapped[str] = mapped_column(
        CHAR(36),  # 改为CHAR(36)以匹配User.user_id
        ForeignKey('users.user_id', ondelete='RESTRICT', onupdate='CASCADE'),
        nullable=False,
        comment="发布者ID（关联users.user_id）"
    )
    
    product_category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('product_categories.category_id', ondelete='RESTRICT', onupdate='CASCADE'),
        nullable=False,
        comment="商品分类ID"
    )
    
    status: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="商品状态：1-上架，0-下架，2-已售"  # 状态更完整
    )
    

    def __repr__(self):
        return f"<Product(product_id={self.product_id}, name={self.product_name}, price={self.product_price})>"