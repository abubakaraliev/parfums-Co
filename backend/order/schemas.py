from pydantic import EmailStr
from app.schemas import CoreModel, DateTimeModelMixin, IDModelMixin


class OrderCreate(CoreModel, DateTimeModelMixin):
    first_name: str
    last_name: str
    email: EmailStr
    address: str
    zipcode: str
    phone: str
    place: str


class OrderInDB(OrderCreate, IDModelMixin):

    class Config:
        orm_mode = True


class OrderItemCreate(CoreModel):
    price: float
    product: int
    quantity: int


class OrderItemInDB(OrderItemCreate, IDModelMixin):
    
    class Config:
        orm_mode = True