from fastapi import FastAPI

from src import __version__
from src.configs.database import Engine
from src.configs.environment import get_environment_variables
from src.middlewares import init_middlewares
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

init_middlewares(app)
init_routes(app)
