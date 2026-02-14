from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import products

router = APIRouter(prefix="/api/product" , tags=["商品"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100,db:AsyncSession = Depends(get_db)):
    categories = await products.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data":categories
    }

@router.get("/homepage")
async def get_homepage_products(
        category_id:int=Query(...,alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", lt=100),
        db:AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    homepage_list = await products.get_homepage_by_category(db, category_id, offset, page_size)
    total = await products.get_product_count_by_category(db, category_id)
    has_more = offset + len(homepage_list) < total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": homepage_list,
            "total": total,
            "hasMore":has_more
        }
    }

@router.get("/list")
async def get_product_list(
        keyword:str=Query(...),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", lt=100),
        db:AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    product_list = await products.get_product_by_keyword(db, keyword, offset, page_size)
    total = await products.get_product_count_by_keyword(db, keyword)
    has_more = offset + len(product_list) < total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": product_list,
            "total": total,
            "hasMore":has_more
        }
    }

@router.get("/detail")
async def get_product_detail(
        product_id:int=Query(...,alias="productId"),
        db:AsyncSession = Depends(get_db)
):
    product = await products.get_product_details(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")


    return {
        "code": 200,
        "message": "success",
        "data": {
            "product_id":product.product_id,
            "product_name": product.product_name,
            "product_price": product.product_price,
            "product_image": product.product_images,
            "product_content": product.product_content,
            "trade_desc": product.trade_desc,
            "create_time": product.created_at,
            "status": product.status
        }
    }