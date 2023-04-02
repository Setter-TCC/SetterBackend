from src.config import BASE_PATH

from fastapi import FastAPI, APIRouter


# Router de checagem de saúde da API
health_check_router = APIRouter()

@health_check_router.get("/health-check")
async def health_check():
    return {"Health Check": "OK"}



def init_routes(app: FastAPI):
    """"
    Função responsável por centralizar a definição de rotas para o serviço
    """
    app.include_router(health_check_router, prefix=BASE_PATH)
    