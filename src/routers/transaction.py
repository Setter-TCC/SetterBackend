from datetime import datetime
from uuid import UUID, uuid4

import pytz
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.transaction import get_transaction_origin, get_transaction_destiny
from src.internal.validators import token_validator, validate_user_authorization
from src.repositories import transacao_repository, integracao_repository
from src.schemas import TransacaoSchema
from src.utils.enums import TipoTransacao
from src.utils.utc import localize

transaction_router = APIRouter(prefix="/transaction", dependencies=[Depends(token_validator)])


@transaction_router.post("/create", tags=["Transação"])
async def create_team_transaction(request: TransacaoSchema, db: Session = Depends(get_db),
                                  token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    request.data_acontecimento = localize(request.data_acontecimento)

    if request.tipo == TipoTransacao.mensalidade.value or request.tipo == TipoTransacao.salario_tecnico.value:
        if not request.pessoa_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="You must link a person to this kind of transaction."
            )

        linked_person = integracao_repository.get_integracoes_by_pessoa_id(db=db, pessoa_id=request.pessoa_id)
        if not linked_person:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="You must link a valid person attached to the team for this kind of transaction."
            )

    if request.data_acontecimento > datetime.now(tz=pytz.timezone('America/Sao_Paulo')):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Future transactions are not allowed to be registered."
        )

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


@transaction_router.get("/", tags=["Transação"])
async def get_specific_transaction(transaction_id: UUID, db: Session = Depends(get_db),
                                   token: dict = Depends(token_validator)):
    transaction = transacao_repository.get_transacao_by_id(db=db, transacao_id=transaction_id)

    if transaction:
        await validate_user_authorization(db, transaction.time_id, token)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching transaction.",
            "value": {
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
            }
        }
    )


@transaction_router.get("/all", tags=["Transação"])
async def get_team_all_transaction(team_id: UUID, db: Session = Depends(get_db),
                                   token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    all_transactions = transacao_repository.get_transacoes_by_time_id(db=db, time_id=team_id)

    if not all_transactions:
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


@transaction_router.get("/month", tags=["Transação"])
async def get_team_month_transaction(team_id: UUID,
                                     month: int = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).month,
                                     year: int = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).year,
                                     db: Session = Depends(get_db),
                                     token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Enter a valid month"
        )

    if year > datetime.now(tz=pytz.timezone('America/Sao_Paulo')).year or year < 1895:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Enter a valid year"
        )

    month_transactions = transacao_repository.get_time_transacoes_by_month(db=db, time_id=team_id,
                                                                           month=month, year=year)

    if not month_transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This team does not have transactions registered for this month."
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
                } for transaction in month_transactions
            ]
        }
    )


@transaction_router.get("/month-type", tags=["Transação"])
async def get_month_type_transaction(team_id: UUID,
                                     type: int,
                                     month: int,
                                     year: int = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).year,
                                     db: Session = Depends(get_db),
                                     token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    if type < 1 or type > 4:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This is not a valid transaction type."
        )

    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Enter a valid month"
        )

    if year > datetime.now(tz=pytz.timezone('America/Sao_Paulo')).year or year < 1895:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Enter a valid year"
        )

    month_type_transactions = transacao_repository.get_time_transacoes_by_month_and_type(db=db, time_id=team_id,
                                                                                         month=month, year=year,
                                                                                         type=type)

    if not month_type_transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This team does not have this kind of transactions registered for this month."
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
                } for transaction in month_type_transactions
            ]
        }
    )


@transaction_router.get("/type", tags=["Transação"])
async def get_type_transaction(team_id: UUID, type: int, db: Session = Depends(get_db),
                               token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    if type < 1 or type > 4:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This is not a valid transaction type."
        )

    type_transactions = transacao_repository.get_time_transacoes_by_tipo(db=db, time_id=team_id,
                                                                         tipo=TipoTransacao(type))

    if not type_transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This team does not have this kind of transactions registered."
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
                } for transaction in type_transactions
            ]
        }
    )


@transaction_router.get("/balance", tags=["Transação"])
async def get_month_balance(team_id: UUID,
                            month: int = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).month,
                            year: int = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).year,
                            db: Session = Depends(get_db),
                            token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Enter a valid month"
        )

    if year > datetime.now(tz=pytz.timezone('America/Sao_Paulo')).year or year < 1895:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Enter a valid year"
        )

    all_transactions = transacao_repository.get_transacoes_by_time_id(db=db, time_id=team_id)

    if not all_transactions:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "msg": "This team has no transactions for this period.",
                "value": {
                    "totalBalance": 0.0,
                    "lastBalance": 0.0
                }
            }
        )

    total_balance: float = 0.0
    last_balance: float = 0.0

    for transaction in all_transactions:
        if (transaction.data_acontecimento.year > year) or (transaction.data_acontecimento.year == year
                                                            and transaction.data_acontecimento.month > month):
            break

        total_balance += transaction.valor
        last_balance += transaction.valor

        if transaction.data_acontecimento.year == year and transaction.data_acontecimento.month == month:
            last_balance -= transaction.valor

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching transactions.",
            "value": {
                "totalBalance": total_balance,
                "lastBalance": last_balance
            }
        }
    )
