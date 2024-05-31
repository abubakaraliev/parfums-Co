from pytest import Session
from .schemas import CategoryCreate, CategoryInDB, ProductCreate, ProductInDB
from .models import Category, Product


async def create_category(db: Session, category: CategoryCreate) -> CategoryInDB:
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return CategoryInDB.from_orm(db_category)

async def create_product(db: Session, product: ProductCreate) -> ProductInDB:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return ProductInDB.from_orm(db_product)