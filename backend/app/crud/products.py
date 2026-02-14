from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Category,Product



async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_homepage_by_category(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 100):
    stmt = select(Product).where(Product.product_category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async  def get_product_count_by_category(db: AsyncSession, category_id: int):
    stmt = select(func.count(Product.product_id)).where(Product.product_category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_product_count_by_keyword(db: AsyncSession, keyword: str):
    stmt = select(func.count(Product.product_id)).where(Product.product_name.like(f"%{keyword}%"))
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_product_by_keyword(db: AsyncSession, keyword: str, skip: int = 0, limit: int = 100):
    stmt = select(Product).where(Product.product_name.like(f"%{keyword}%")).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_product_details(db: AsyncSession, product_id: int):
    stmt = select(Product).where(Product.product_id == product_id)
    result = await db.execute(stmt)
    return result.scalar_one()