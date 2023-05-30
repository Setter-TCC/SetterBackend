from fastapi import FastAPI, APIRouter

from src.configs.environment import get_environment_variables
from src.routers.account import account_router

env = get_environment_variables()

# Router de checagem de saúde da API
health_check_router = APIRouter()


@health_check_router.get("/health-check")
async def health_check():
    return {"Health Check": "OK"}


def init_routes(app: FastAPI):
    """"
    Função responsável por centralizar a definição de rotas para o serviço
    """
    BASE_PATH = env.BASE_PATH

    app.include_router(health_check_router, prefix=BASE_PATH)
    app.include_router(account_router, prefix=BASE_PATH)
