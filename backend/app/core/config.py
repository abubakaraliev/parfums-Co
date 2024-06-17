import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    

    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    DATABASE_URI: Optional[str] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql://{values.get('MYSQL_USER')}:{values.get('MYSQL_PASSWORD')}@{values.get('MYSQL_HOST')}:" \
               f"{values.get('MYSQL_PORT')}/{values.get('MYSQL_DATABASE')}"

    class Config:
        case_sensitive = True
        env_file = ".env"

        
    
    JWT_SETTINGS: Optional[Dict[str, Any]] = None
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_TOKEN_PREFIX: str
    JWT_AUDIENCE: str

    @validator('JWT_SETTINGS', pre=True)
    def assemble_jwt_settings(cls, v: Optional[Dict[str, Any]], values: Dict[str, Any]) -> Dict[str, Any]:
        if v is None:
            return {
                "SECRET_KEY": values.get("SECRET_KEY"),
                "JWT_ALGORITHM": values.get("JWT_ALGORITHM"),
                "ACCESS_TOKEN_EXPIRE_MINUTES": values.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
                "JWT_TOKEN_PREFIX": values.get("JWT_TOKEN_PREFIX"),
                "JWT_AUDIENCE": values.get("JWT_AUDIENCE"),
            }
        return v


settings = Settings()

