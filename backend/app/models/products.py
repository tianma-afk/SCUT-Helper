from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

class Category(Base):
    __tablename__ = "product_categories"

    category_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="分类id"
    )
    category_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="分类名称"
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name})>"

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="商品id"
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
    product_category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('product_categories.category_id'),
        nullable=False,
        comment="商品分类id"
    )
    product_content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="商品详细内容"
    )
    product_images:Mapped[Optional[str]] = mapped_column(
        String(2048),
        comment="商品图片URL，多个用英文逗号分隔"
    )
    trade_desc : Mapped[str] = mapped_column(
        String(512),
        comment="商品交易描述"
    )
    #publisher_id目前没有用户表可以关联
    publisher_id: Mapped[int] = mapped_column(  # 明确类型
        Integer,
        nullable=False,
        comment="发布者ID"
    )
    status: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="商品状态：1-上架，2-下架，3-已售"
    )

    def __repr__(self):
        return f"<Product(id={self.product_id}, name={self.product_name, self.product_content})>"