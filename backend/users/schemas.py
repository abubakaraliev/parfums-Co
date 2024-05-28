from datetime import datetime, timedelta
import string
from pydantic import EmailStr, constr, validator
from app.schemas import CoreModel, DateTimeModelMixin, IDModelMixin
from typing import Optional
from app.core.config import settings

# JWT
class JWTMeta(CoreModel):
    iss: str = "localhost"
    aud: str = settings.JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.now())
    exp: float = datetime.timestamp(
        datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))


class JWTCreds(CoreModel):

    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):

    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str

# USER
def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(
        char in allowed for char in username), "Invalid characters in username."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username


class UserBase(CoreModel):

    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(CoreModel):

    email: EmailStr
    password: str
    username: str

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)

    @validator("password")
    def password_length(cls, password: str) -> str:
        if len(password) < 7:
            raise ValueError("Password length must be at least 7 characters")
        elif len(password) > 100:
            raise ValueError("Password length cannot exceed 100 characters")
        return password

    class Config:
        orm_mode = True


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    id: str
    password: str
    salt: str

    class Config:
        orm_mode = True


class UserPublic(DateTimeModelMixin, UserBase):
    access_token: Optional[AccessToken]

    class Config:
        orm_mode = True


# TODO: UserUpdate for updating user details can be here

# TODO: UserPasswordUpdate for password update can be here

class UserPasswordUpdate(CoreModel):

    password: str
    salt: str

    class Config:
        orm_mode = True


class UserLogin(CoreModel):
    """
    username and password are required for logging in the user
    """
    username: str
    password: str

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)

    @validator("password")
    def password_length(cls, password: str) -> str:
        if len(password) < 7:
            raise ValueError("Password length must be at least 7 characters")
        elif len(password) > 100:
            raise ValueError("Password length cannot exceed 100 characters")
        return password
