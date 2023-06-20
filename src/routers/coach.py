from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.coach import generate_payload_for_coach_create, generate_payload_for_coach_update
from src.internal.validators import validate_user_authorization, token_validator
from src.repositories import integracao_repository, pessoa_repository, tecnico_repository
from src.schemas import TreinadorRequest, TecnicoActivationRequest, EditTreinadorRequest

coach_router = APIRouter(prefix="/coach", dependencies=[Depends(token_validator)])


@coach_router.post("/create", tags=["Técnico"])
async def create_coach(request: TreinadorRequest, db: Session = Depends(get_db),
                       token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    active_coaches = tecnico_repository.get_coach_from_team(db=db, time_id=request.time_id)
    if len(active_coaches) >= 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "msg": "This team already has a coach registered."
            }
        )

    request.id = uuid4()
    tecnico, integracao, pessoa_atleta = generate_payload_for_coach_create(request)

    pessoa_tecnico_ok = pessoa_repository.create_pessoa(db=db, pessoa=pessoa_atleta)
    if not pessoa_tecnico_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not create person entity on database."
        )

    tecnico_ok = tecnico_repository.create_tecnico(db=db, tecnico=tecnico)
    if not tecnico_ok:
        db.rollback()
        pessoa_repository.delete_pessoa(db=db, pessoa_id=pessoa_atleta.id)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not create coach entity on database."
        )

    integracao_ok = integracao_repository.create_integracao(db=db, integracao=integracao)
    if not integracao_ok:
        db.rollback()
        pessoa_repository.delete_pessoa(db=db, pessoa_id=pessoa_atleta.id)
        tecnico_repository.delete_tecnico(db=db, id_tecnico=tecnico.id)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not link person to given team."
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "msg": "Created coach successfully",
            "fields": {
                "athlete": "Coach created successfully.",
            },
        }
    )


@coach_router.get("", tags=["Técnico"])
async def get_active_coach_from_team(team_id: UUID, db: Session = Depends(get_db),
                                     token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    coach = tecnico_repository.get_coach_from_team(db=db, time_id=team_id)

    if len(coach) > 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This team has more than 1 active coach."
        )

    if len(coach) < 1:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detal": "This team has no coaches."
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching coach.",
            "value": {
                "id": str(coach.Pessoa.id),
                "nome": coach.Pessoa.nome,
                "email": coach.Pessoa.email,
                "data_nascimento": coach.Pessoa.data_nascimento.strftime(
                    "%d/%m/%Y") if coach.Pessoa.data_nascimento else None,
                "cpf": coach.Pessoa.cpf,
                "rg": coach.Pessoa.rg,
                "telefone": coach.Pessoa.telefone,
                "cref": coach.Treinador.cref,
                "data_inicio": coach.IntegracaoIntegra.data_inicio.strftime("%d/%m/%Y")
            }
        }
    )


@coach_router.post("/deactivate", tags=["Técnico"])
async def deactivate_coach(request: TecnicoActivationRequest, db: Session = Depends(get_db),
                           token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    integracao = integracao_repository.get_integracao_by_user_and_team_id(db=db, user_id=request.tecnico_id,
                                                                          team_id=request.time_id)
    if not integracao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link between coach and team not found."
        )

    update_ok = integracao_repository.remove_from_team(db=db, integration_id=integracao.id)
    if not update_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Could not deactivate the coach."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Deactivated coach succesfully"
        }
    )


@coach_router.put("/update", tags=["Técnico"])
async def update_coach(request: EditTreinadorRequest, db: Session = Depends(get_db),
                       token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    tecnico, pessoa, integracao_tecnico = generate_payload_for_coach_update(db=db, request=request)

    if integracao_tecnico.data_fim is not None:
        if integracao_tecnico.data_fim > integracao_tecnico.data_inicio:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "msg": "End date must be grather than start date."
                }
            )

    pessoa_ok = pessoa_repository.update_pessoa(db=db, pessoa=pessoa)
    if not pessoa_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Could not update personal data from the coach."
        )

    tecnico_ok = tecnico_repository.update_tecnico(db=db, tecnico=tecnico)
    if not tecnico_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Could not update sport data from the coach."
        )

    integracao_ok = integracao_repository.update_integracao(db=db, integracao=integracao_tecnico)
    if not integracao_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Could not update team data from the coach."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Updated coach succesfully."
        }
    )
