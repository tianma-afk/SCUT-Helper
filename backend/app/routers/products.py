from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import products
from utils.auth import get_current_user
from models.users import User
router = APIRouter(prefix="/product" , tags=["商品"])

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


@router.post("/add")
async def add_product(
        product_name: str = Query(..., description="商品名称"),
        product_price: float = Query(..., description="商品价格"),
        product_content: str = Query(..., description="商品详细内容"),
        product_images: str = Query(None, description="商品图片 URL，多个用英文逗号分隔"),
        trade_desc: str = Query(None, description="商品交易描述"),
        product_category_id: int = Query(..., description="商品分类 ID"),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    try:
        new_product = await products.create_product(
            db=db,
            product_name=product_name,
            product_price=product_price,
            product_content=product_content,
            product_images=product_images,
            trade_desc=trade_desc,
            publisher_id=current_user.user_id,
            product_category_id=product_category_id
        )

        return {
            "code": 200,
            "message": "success",
            "data": {
                "product_id": new_product.product_id
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update")
async def update_product(
        product_id: int = Query(..., description="商品 ID"),
        product_name: str = Query(None, description="商品名称"),
        product_price: float = Query(None, description="商品价格"),
        product_content: str = Query(None, description="商品详细内容"),
        product_images: str = Query(None, description="商品图片 URL"),
        trade_desc: str = Query(None, description="商品交易描述"),
        product_category_id: int = Query(None, description="商品分类 ID"),
        status: int = Query(None, description="商品状态：1-上架，0-下架，2-已售"),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    try:
        updated_product = await products.update_product(
            db=db,
            product_id=product_id,
            publisher_id=current_user.user_id,
            product_name=product_name,
            product_price=product_price,
            product_content=product_content,
            product_images=product_images,
            trade_desc=trade_desc,
            product_category_id=product_category_id,
            status=status
        )

        if not updated_product:
            raise HTTPException(status_code=404, detail="商品不存在")

        return {
            "code": 200,
            "message": "success",
            "data": None
        }
    except PermissionError:
        raise HTTPException(status_code=403, detail="无权限修改该商品")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete")
async def delete_product(
        product_id: int = Query(..., description="商品 ID"),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    try:
        success = await products.delete_product(
            db=db,
            product_id=product_id,
            publisher_id=current_user.user_id
        )

        if not success:
            raise HTTPException(status_code=404, detail="商品不存在")

        return {
            "code": 200,
            "message": "success",
            "data": None
        }
    except PermissionError:
        raise HTTPException(status_code=403, detail="无权限删除该商品")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))