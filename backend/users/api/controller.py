from fastapi import APIRouter, Body, Depends, HTTPException
from ..schemas import AccessToken, UserCreate, UserInDB, UserLogin, UserPublic
from users import auth_service
from users.crud import create_user, get_user_by_username
from users.authentication import get_current_active_user

router = APIRouter()

# Register the User
@router.post(
    "/create",
    tags=["user registration"],
    description="Register the User",
    response_model=UserPublic,
)
def user_create(new_user: UserCreate):
    return create_user(new_user=new_user)

# Log in the User
@router.post(
    '/login',
    tags=["user login"],
    description="Log in the User",
    response_model=UserPublic
)
def user_login(user: UserLogin) -> UserPublic:
    found_user = get_user_by_username(username=user.username)
    if not found_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if auth_service.verify_password(password=user.password, salt=found_user.salt, hashed_pw=found_user.password):
        token = auth_service.create_access_token_for_user(user=found_user)
        if not token:
            raise HTTPException(status_code=500, detail="Token generation failed")
        
        access_token = AccessToken(access_token=token, token_type='bearer')
        return UserPublic(**found_user.dict(), access_token=access_token)
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
@router.get(
    "/me",
    tags=["get current logged in user"],
    description="Get current logged in user",
    response_model=UserPublic,
)
def get_me(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
    return current_user
