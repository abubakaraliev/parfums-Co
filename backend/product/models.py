from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Integer
from app.database import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), unique=True, nullable=False)
    slug = Column(String(length=255), unique=True, nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer(), primary_key=True)
    category = Column(Integer(), ForeignKey('category.id'))
    name = Column(String(length=255), unique=True, nullable=False)
    slug = Column(String(length=255), unique=True, nullable=False)
    description = Column(String(length=255), nullable=True)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    thumbnail = Column(String(length=255), nullable=True)
    date_added = Column(DateTime(), nullable=False)
