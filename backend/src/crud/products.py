from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Category,Product
from sqlalchemy import select, func, update, delete

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
    return result.scalar_one_or_none()

async def create_product(
        db: AsyncSession,
        product_name: str,
        product_price: float,
        product_content: str,
        product_images: str,
        trade_desc: str,
        publisher_id: str,
        product_category_id: int
):

    new_product = Product(
        product_name=product_name,
        product_price=product_price,
        product_content=product_content,
        product_images=product_images,
        trade_desc=trade_desc,
        publisher_id=publisher_id,
        product_category_id=product_category_id,
        status=1  # 默认上架状态
    )

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

async def update_product(
        db: AsyncSession,
        product_id: int,
        publisher_id: str,
        product_name: str = None,
        product_price: float = None,
        product_content: str = None,
        product_images: str = None,
        trade_desc: str = None,
        product_category_id: int = None,
        status: int = None
):

    # 先查询商品是否存在且属于该发布者
    product = await get_product_details(db, product_id)
    if not product:
        return None

    if product.publisher_id != publisher_id:
        raise PermissionError("无权限修改该商品")

    # 构建更新字段
    update_data = {}
    if product_name is not None:
        update_data['product_name'] = product_name
    if product_price is not None:
        update_data['product_price'] = product_price
    if product_content is not None:
        update_data['product_content'] = product_content
    if product_images is not None:
        update_data['product_images'] = product_images
    if trade_desc is not None:
        update_data['trade_desc'] = trade_desc
    if product_category_id is not None:
        update_data['product_category_id'] = product_category_id
    if status is not None:
        update_data['status'] = status

    if update_data:
        stmt = update(Product).where(Product.product_id == product_id).values(**update_data)
        await db.execute(stmt)
        await db.commit()
        await db.refresh(product)

    return product


async def delete_product(
        db: AsyncSession,
        product_id: int,
        publisher_id: str
):
    # 先查询商品是否存在且属于该发布者
    product = await get_product_details(db, product_id)
    if not product:
        return None

    if product.publisher_id != publisher_id:
        raise PermissionError("无权限删除该商品")

    stmt = delete(Product).where(Product.product_id == product_id)
    await db.execute(stmt)
    await db.commit()
    return True