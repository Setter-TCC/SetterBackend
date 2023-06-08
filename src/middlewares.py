from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_middlewares(app: FastAPI):
    origins = ['*']

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"],
    )
