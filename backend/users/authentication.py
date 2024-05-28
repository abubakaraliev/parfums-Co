from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings
import bcrypt, jwt
from passlib.context import CryptContext
from .schemas import JWTCreds, JWTMeta, JWTPayload, UserInDB, UserPasswordUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Authenticate:
    def create_salt_and_hashed_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(
            password=plaintext_password, salt=salt)
        return UserPasswordUpdate(salt=salt, password=hashed_password)

    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().encode().decode()

    @staticmethod
    def hash_password(*, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    @staticmethod
    def verify_password(*, password: str, salt: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password + salt, hashed_pw)

    @staticmethod
    def create_access_token_for_user(
        *,
        user: UserInDB,
        secret_key: str = str(settings.SECRET_KEY),
        audience: str = settings.JWT_AUDIENCE,
        expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> Optional[str]:
        if not user or not isinstance(user, UserInDB):
            print("Invalid user or user type.")
            return None

        try:
            jwt_meta = JWTMeta(
                aud=audience,
                iat=datetime.timestamp(datetime.now()),
                exp=datetime.timestamp(datetime.now() + timedelta(minutes=expires_in)),
            )
            jwt_creds = JWTCreds(sub=user.email, username=user.username)
            token_payload = JWTPayload(
                **jwt_meta.dict(),
                **jwt_creds.dict(),
            )

            token = jwt.encode(
                token_payload.dict(), secret_key, algorithm=settings.JWT_ALGORITHM
            )

            print("Token payload:", token_payload.dict())
            print("Generated token:", token)

            return token
        except Exception as e:
            print(f"Token generation error: {e}")
            return None
