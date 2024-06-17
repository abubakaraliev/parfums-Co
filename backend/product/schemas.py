from datetime import datetime
from typing import Optional
from app.schemas import CoreModel, DateTimeModelMixin, IDModelMixin


class CategoryCreate(CoreModel):
    name: str
    slug: str


class CategoryInDB(CategoryCreate, IDModelMixin):

    class Config:
        orm_mode = True
        
class ProductCreate(CoreModel, DateTimeModelMixin):
    category: int
    name: str
    slug: str
    description: Optional[str]
    price: float
    image: Optional[str]
    thumbnail: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime] 


class ProductInDB(ProductCreate, IDModelMixin):
    id: int
    category: int
    name: str
    slug: str
    description: Optional[str]
    price: float
    image: Optional[str]
    thumbnail: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True