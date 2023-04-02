from fastapi import FastAPI

from src import __version__
from src.config import BASE_PATH
from src.router import init_routes


app = FastAPI(
    title="SETTER",
    version=__version__,
    description="API REST relativa ao Setter, software especializado em gestão desportiva de times de vôlei.",
    docs_url=f"{BASE_PATH}/docs",
    redoc_url=f"{BASE_PATH}/redoc",
    openapi_url=f"{BASE_PATH}/openapi.json"
)

init_routes(app)
