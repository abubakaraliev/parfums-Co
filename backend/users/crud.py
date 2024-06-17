import uuid
from .models import User
from datetime import datetime
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from .schemas import UserCreate, UserInDB, UserUpdate
from sqlalchemy.orm import Session
from app.database import SessionLocal


def create_user(new_user: UserCreate) -> UserInDB:
    from users import auth_service
    new_password = auth_service.create_salt_and_hashed_password(
        plaintext_password=new_user.password)
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

def update_user(db: Session, user_id: str, user_update: UserUpdate) -> UserInDB:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    
    if 'username' in update_data:
        existing_user = db.query(User).filter(User.username == update_data['username']).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="Username already taken")

    if 'password' in update_data:
        from users import auth_service
        new_password_data = auth_service.create_salt_and_hashed_password(
            plaintext_password=update_data['password'])
        update_data['password'] = new_password_data.password
        update_data['salt'] = new_password_data.salt
    
    update_data['updated_at'] = datetime.now()
    
    for key, value in update_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return UserInDB.from_orm(user)


def delete_user(user_id: str) -> UserInDB:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
    return UserInDB.from_orm(user)


def get_all_users(users: str) -> List[UserInDB]:
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [UserInDB.from_orm(user) for user in users]
