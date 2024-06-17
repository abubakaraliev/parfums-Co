from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from product.crud import create_product, delete_product_by_id
from app.helpers import handle_file_upload
from users import check_if_user_is_admin
from product.models import Product
from ..schemas import CategoryInDB, CategoryCreate, ProductCreate, ProductInDB

router = APIRouter()


@router.post(
    "/category/create",
    tags=["create category"],
    description="Create new category",
    response_model=CategoryInDB,
    dependencies=[Depends(check_if_user_is_admin)]
)
def category_create(category: CategoryCreate) -> CategoryInDB:
    from product.crud import create_category
    return create_category(category)


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

    try:
        image_path, thumbnail_path = await handle_file_upload(image)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    product_data = ProductCreate(
        category=category,
        name=name,
        slug=slug,
        price=price,
        description=description,
        image=image_path,
        thumbnail=thumbnail_path
    )

    created_product = create_product(db, product_data)

    return created_product


@router.get("/all",
            tags=["get products"],
            description="Get all products",
            response_model=List[ProductInDB])
def get_all_products() -> List[ProductInDB]:
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        return products
    finally:
        db.close()


@router.delete("/delete/{product_id}",
               tags=["delete product"],
               description="Delete product by ID",
               dependencies=[Depends(check_if_user_is_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    delete_product_by_id(product_id, db)
    
    return {"message": "Product deleted successfully"}

