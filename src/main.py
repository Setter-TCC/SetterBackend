from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from src import __version__
from src.configs.database import Engine
from src.configs.environment import get_environment_variables
from src.models import Base
from src.router import init_routes

env = get_environment_variables()
Base.metadata.create_all(bind=Engine)

app = FastAPI(  # TODO: Padronizar a linguagem de escrita do app
    title="SETTER",
    version=__version__,
    description="API REST relativa ao Setter, software especializado em gestão desportiva de times de vôlei.",
    docs_url=f"{env.BASE_PATH}/docs",
    redoc_url=f"{env.BASE_PATH}/redoc",
    openapi_url=f"{env.BASE_PATH}/openapi.json"
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

init_routes(app)
