from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.transaction import get_transaction_origin, get_transaction_destiny
from src.internal.validators import token_validator, validate_user_authorization
from src.repositories import transacao_repository
from src.schemas import TransacaoSchema
from src.utils.enums import TipoTransacao

transaction_router = APIRouter(prefix="/transaction", dependencies=[Depends(token_validator)])


@transaction_router.post("/create", tags=["Transação"])
async def create_team_transaction(request: TransacaoSchema, db: Session = Depends(get_db),
                                  token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)
    request.id = uuid4()
    request.valor = abs(request.valor)

    if request.tipo == TipoTransacao.salario_tecnico.value or request.tipo == TipoTransacao.despesa.value:
        request.valor *= (-1)

    transacao_ok = transacao_repository.create_transacao(db=db, transacao=request)
    if not transacao_ok:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not create transaction"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Created transaction succesfully.",
        }
    )


@transaction_router.get("/all", tags=["Transação"])
async def get_team_all_transaction(team_id: UUID, db: Session = Depends(get_db),
                                   token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    all_transactions = transacao_repository.get_transacoes_by_time_id(db=db, time_id=team_id)

    if len(all_transactions) == 0 or not all_transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This team does not have transactions registered."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching transactions.",
            "value": [
                {
                    "id": str(transaction.id),
                    "nome": transaction.nome,
                    "descricao": transaction.descricao,
                    "data_acontecimento": transaction.data_acontecimento.strftime("%d/%m/%Y"),
                    "tipo": transaction.tipo.value,
                    "valor": transaction.valor,
                    "origem": get_transaction_origin(
                        team_name=transaction.time.nome,
                        transaction_name=transaction.nome,
                        person_name=transaction.pessoa.nome if transaction.pessoa else "",
                        tipo_transacao=transaction.tipo
                    ),
                    "destino": get_transaction_destiny(
                        team_name=transaction.time.nome,
                        transaction_name=transaction.nome,
                        person_name=transaction.pessoa.nome if transaction.pessoa else "",
                        tipo_transacao=transaction.tipo
                    )
                } for transaction in all_transactions
            ]
        }
    )
