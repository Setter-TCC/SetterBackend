from datetime import datetime
from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.validators import token_validator, validate_user_authorization
from src.repositories import time_repository, admin_repository, integracao_repository
from src.schemas import TimeSchema, IntegracaoIntegraSchema
from src.utils.enums import TipoPessoa

team_router = APIRouter(prefix="/team", dependencies=[Depends(token_validator)])


@team_router.post("/create", tags=["Time"])
async def create_team(request: TimeSchema, db: Session = Depends(get_db), token: dict = Depends(token_validator)):
    username = token.get("sub")
    admin = admin_repository.get_admin_by_nome_usuario(db=db, nome_usuario=username)
    request.id = uuid4()

    integracao = IntegracaoIntegraSchema(
        id=uuid4(),
        data_inicio=datetime.now(),
        ativo=True,
        tipo_pessoa=TipoPessoa.administrador,
        time_id=request.id,
        pessoa_id=admin.id
    )

    time_ok = time_repository.create_time(db=db, time=request)
    if not time_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not create team on database."
        )

    integracao_ok = integracao_repository.create_integracao(db=db, integracao=integracao)
    if not integracao_ok:
        db.rollback()
        time_repository.delete_time(db=db, time_id=request.id)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not link team and admin. Team was not created."
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "msg": "Created team succesfully successfully",
            "fields": {
                "team": "Team created successfully.",
                "integration": "Link between team and admin created successfully."
            }
        }
    )


@team_router.get("", tags=["Time"])
async def get_team_data(team_id: UUID, db: Session = Depends(get_db), token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)
    team = time_repository.get_time_by_id(db=db, time_id=team_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching team.",
            "value": {
                "id": str(team.id),
                "nome": team.nome,
                "email": team.email,
                "naipe": team.naipe.value,
                "cnpj": team.cnpj
            }
        }
    )


@team_router.put("/update", tags=["Time"])
async def update_team(request: TimeSchema, db: Session = Depends(get_db), token: dict = Depends(token_validator)):
    if not request.id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Request body is not well formated."
        )

    await validate_user_authorization(db, request.id, token)

    time_ok = time_repository.update_time(db=db, time=request)
    if not time_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Team could not be updated."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Updated team succesfully."
        }
    )
