from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Integer
from app.database import Base

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(length=255), ForeignKey('user.id'))
    first_name = Column(String(length=20))
    last_name = Column(String(length=20))
    email = Column(String(length=50))
    address = Column(String(length=100))
    zipcode = Column(String(length=10))
    place = Column(String(length=50))
    phone = Column(String(length=15))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
    paid_amount = Column(Numeric(), nullable=False)
    stripe_token = Column(String(length=100))
    
class OrderItem(Base):
    __tablename__ = 'orderitem'
    id = Column(Integer, primary_key=True, index=True)
    order = Column(Integer, ForeignKey('order.id'))
    product = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, server_default='1')
    price = Column(Numeric(), nullable=False)
    