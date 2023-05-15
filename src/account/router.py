from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import src.account.service as account_service
from src.utils import get_db, GenericResponse
from src.schemas import Pessoa as PessoaSchema
from src.schemas import PessoaRequest

account_router = APIRouter(prefix="/account")

@account_router.get("/")
async def get(db: Session = Depends(get_db)):
    _pessoas = account_service.get_pessoas(db=db)
    return GenericResponse(
        code=200,
        message="Tudo certo ao buscar suas pessoas",
        value=_pessoas
    ).dict(exclude_none=True)

@account_router.post("/")
async def create(request: PessoaRequest, db: Session = Depends(get_db)):
    account_service.create_pessoa(db, request.parameter)
    return GenericResponse(
        code=200,
        message="Pessoa criada com sucesso",
    ).dict(exclude_none=True)
