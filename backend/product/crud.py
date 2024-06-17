from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .schemas import CategoryCreate, CategoryInDB, ProductCreate, ProductInDB
from .models import Category, Product
from typing import List
from app.database import SessionLocal


def create_category(category: CategoryCreate) -> CategoryInDB:
    created_category = Category(**category.dict())
    return CategoryInDB.from_orm(created_category)


def create_product(db: Session, product: ProductCreate) -> ProductInDB:
    db = SessionLocal()
    try:

        new_product = Product(
            category=product.category,
            name=product.name,
            description=product.description,
            slug=product.slug,
            price=product.price,
            image=product.image,
            thumbnail=product.thumbnail,
            created_at=product.created_at or datetime.now(),
            updated_at=product.updated_at or datetime.now()
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return ProductInDB.from_orm(new_product)

    except IntegrityError:
        db.rollback()
        raise ValueError("Product with this name already exists.")

    finally:
        db.close()


def get_all_categories() -> List[CategoryInDB]:
    db = SessionLocal()
    try:
        return db.query(Category).all()
    finally:
        db.close()


def get_all_products() -> List[ProductInDB]:
    db = SessionLocal()
    try:
        return db.query(Product).all()
    finally:
        db.close()


def get_products_by_category(category_id: int) -> List[ProductInDB]:
    db = SessionLocal()
    try:
        return db.query(Product).filter(Product.category_id == category_id).all()
    finally:
        db.close()
        

def delete_product_by_id(product_id: int, db: Session) -> None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Product not found")
        db.close()
