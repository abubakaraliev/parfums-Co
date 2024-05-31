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


class ProductInDB(ProductCreate, IDModelMixin):
    
    class Config:
        orm_mode = True