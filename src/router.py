from fastapi import FastAPI, APIRouter

from src.configs.environment import get_environment_variables
from src.routers.account import account_router
from src.routers.admin import admin_router
from src.routers.athlete import athlete_router
from src.routers.coach import coach_router
from src.routers.evento import evento_router
from src.routers.team import team_router
from src.routers.token import token_router
from src.routers.transaction import transaction_router

env = get_environment_variables()

# Router de checagem de saúde da API
health_check_router = APIRouter()


@health_check_router.get("/health-check", tags=["Health-Check"])
async def health_check():
    return {"Health Check": "OK"}


def init_routes(app: FastAPI):
    """"
    Função responsável por centralizar a definição de rotas para o serviço
    """
    BASE_PATH = env.BASE_PATH

    app.include_router(health_check_router, prefix=BASE_PATH)
    app.include_router(account_router, prefix=BASE_PATH)
    app.include_router(team_router, prefix=BASE_PATH)
    app.include_router(token_router, prefix=BASE_PATH)
    app.include_router(athlete_router, prefix=BASE_PATH)
    app.include_router(coach_router, prefix=BASE_PATH)
    app.include_router(admin_router, prefix=BASE_PATH)
    app.include_router(transaction_router, prefix=BASE_PATH)
    app.include_router(evento_router, prefix=BASE_PATH)
