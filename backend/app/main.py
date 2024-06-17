import sys
import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users.api.controller import router as user_router
from product.api.controller import router as product_router
from app.core.config import settings

sys.path.append('..')

BASEDIR = os.path.dirname(__file__)


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.include_router(user_router, prefix='/users')

    _app.include_router(product_router, prefix='/product')

    _app.mount("/static", StaticFiles(directory=BASEDIR +
               "/statics"), name="static")

    # origins = [
    #     "http://localhost",
    #     "http://localhost:3000",
    #     "http://0.0.0.0"
    #     "http://0.0.0.0:3000",
    #     "http://127.0.0.1:3000",
    # ]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
