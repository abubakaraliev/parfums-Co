from sqlalchemy import Column, String, Unicode, DateTime, Boolean
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(), primary_key=True)
    username = Column(Unicode(), unique=True, nullable=False)
    email = Column(String(), unique=True, nullable=False)
    email_verified = Column(Boolean(), nullable=True, server_default="True")
    salt = Column(Unicode(), nullable=False)
    password = Column(Unicode(), nullable=False)
    is_active = Column(Boolean(), nullable=False, server_default="True")
    is_superuser = Column(Boolean(), nullable=False, server_default="False")
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
