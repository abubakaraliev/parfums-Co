import sys, os
from fastapi.staticfiles import StaticFiles
from .database import Base, engine, get_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users.api.controller import router as user_router
from product.api.controller import router as product_router
from app.core.config import settings

sys.path.append('..')

BASEDIR = os.path.dirname(__file__)


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(user_router, prefix='/users')
    
    _app.include_router(product_router, prefix='/product')
    
    _app.mount("/static", StaticFiles(directory=BASEDIR + "/statics"), name="static")

    return _app


app = get_application()
