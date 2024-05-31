from typing import Optional
import uuid
from sqlalchemy.exc import IntegrityError
from .schemas import UserCreate, UserInDB
from .models import User
from app.database import SessionLocal

def create_user(new_user: UserCreate) -> UserInDB:
    from users import auth_service
    new_password = auth_service.create_salt_and_hashed_password(plaintext_password=new_user.password)
    new_user_params = new_user.dict()
    new_user_params["id"] = str(uuid.uuid4())
    new_user_params.update(new_password.dict())
    new_user_updated = UserInDB(**new_user_params)
    print(new_user_updated)

    db = SessionLocal()
    try:
        db_user = User(**new_user_updated.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this email already exists.")
    finally:
        db.close()

    return new_user_updated

def get_user_by_username(username: str) -> Optional[UserInDB]:
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user:
        return UserInDB.from_orm(user)
    return None