from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.database import get_db
from product.crud import create_category, create_product
from app.helpers import handle_file_upload
from ..schemas import CategoryInDB, CategoryCreate, ProductCreate, ProductInDB
from sqlalchemy.orm import Session
from users import check_if_user_is_admin

router = APIRouter()

@router.post(
    "/category/create",
    tags=["create category"],
    description="Create new category",
    response_model=CategoryInDB,
    dependencies=[Depends(check_if_user_is_admin)]
)
async def category_create(category: CategoryCreate, db: Session = Depends(get_db)) -> CategoryInDB:
    return await create_category(db, category)


@router.post(
    "/product/create",
    tags=["create product"],
    description="Create new product",
    response_model=ProductInDB,
    dependencies=[Depends(check_if_user_is_admin)]
)
async def product_create(
    category: int = Form(...),
    name: str = Form(...),
    slug: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> ProductInDB:
    product_data = ProductCreate(
        category=category,
        name=name,
        slug=slug,
        price=price,
        description=description
    )
    product_data.image = await handle_file_upload(image)

    return await create_product(db, product_data)

# async def product_create(product: ProductCreate, db: Session = Depends(get_db)) -> ProductInDB:
#     return await create_product(db, product)