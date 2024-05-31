from sqlalchemy import Column, String, Unicode, DateTime, Boolean
from app.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String(length=255), primary_key=True, nullable=False)
    username = Column(String(length=255), nullable=False, unique=True)
    email = Column(String(length=255), nullable=False, unique=True)
    email_verified = Column(Boolean, default=True)
    salt = Column(String(length=255), nullable=False)
    password = Column(String(length=255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)