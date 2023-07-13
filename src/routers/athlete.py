from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.athlete import generate_payload_for_athlete_create
from src.internal.validators import validate_user_authorization, token_validator
from src.repositories import integracao_repository, pessoa_repository, atleta_repository
from src.schemas import AtletaRequest, AtletaActivationRequest, PessoaSchema, AtletaSchema

athlete_router = APIRouter(prefix="/athlete", dependencies=[Depends(token_validator)])


@athlete_router.post("/create", tags=["Atletas"])
async def create_atletas(request: AtletaRequest, db: Session = Depends(get_db),
                         token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    atleta, integracao, pessoa_atleta = generate_payload_for_athlete_create(request)

    pessoa_atleta_ok = pessoa_repository.create_pessoa(db=db, pessoa=pessoa_atleta)
    if not pessoa_atleta_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not create person entity on database."
        )

    atleta_ok = atleta_repository.create_atleta(db=db, atleta=atleta)
    if not atleta_ok:
        db.rollback()
        pessoa_repository.delete_pessoa(db=db, pessoa_id=pessoa_atleta.id)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not create athlete entity on database."
        )

    integracao_ok = integracao_repository.create_integracao(db=db, integracao=integracao)
    if not integracao_ok:
        db.rollback()
        pessoa_repository.delete_pessoa(db=db, pessoa_id=pessoa_atleta.id)
        atleta_repository.delete_atleta(db=db, id_atleta=atleta.id)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not link person to given team."
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "msg": "Created athlete successfully",
            "fields": {
                "athlete": "Athlete created successfully.",
            },
        }
    )


@athlete_router.get("", tags=["Atletas"])
async def get_atletas_from_time(team_id: UUID, db: Session = Depends(get_db),
                                token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    atletas = atleta_repository.get_atletas_time(db=db, time_id=team_id)
    if not atletas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This team has no athletes registered."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching all athletes.",
            "value": [
                {
                    "id": str(atleta.Pessoa.id),
                    "nome": atleta.Pessoa.nome,
                    "email": atleta.Pessoa.email,
                    "data_nascimento": atleta.Pessoa.data_nascimento.strftime(
                        "%d/%m/%Y") if atleta.Pessoa.data_nascimento else None,
                    "cpf": atleta.Pessoa.cpf,
                    "rg": atleta.Pessoa.rg,
                    "telefone": atleta.Pessoa.telefone,
                    "posicao": atleta.Atleta.posicao.value,
                    "ativo": atleta.IntegracaoIntegra.ativo
                } for atleta in atletas
            ]
        }
    )


@athlete_router.get("/active-athletes", tags=["Atletas"])
async def get_active_atletas_from_time(team_id: UUID, active: bool = True, db: Session = Depends(get_db),
                                       token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)
    active_status = "active" if active else "disabled"
    atletas = atleta_repository.get_active_atletas_time(db=db, time_id=team_id, active=active)
    if not atletas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This team has no {active_status} athletes registered."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": f"Success fetching all {active_status} athletes.",
            "value": [
                {
                    "id": str(atleta.Pessoa.id),
                    "nome": atleta.Pessoa.nome,
                    "email": atleta.Pessoa.email,
                    "data_nascimento": atleta.Pessoa.data_nascimento.strftime(
                        "%d/%m/%Y") if atleta.Pessoa.data_nascimento else None,
                    "cpf": atleta.Pessoa.cpf,
                    "rg": atleta.Pessoa.rg,
                    "telefone": atleta.Pessoa.telefone,
                    "posicao": atleta.Atleta.posicao.value,
                } for atleta in atletas
            ]
        }
    )


@athlete_router.post("/deactivate", tags=["Atletas"])
async def deactivate_athlete(request: AtletaActivationRequest, db: Session = Depends(get_db),
                             token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    integracao = integracao_repository.get_integracao_by_user_and_team_id(db=db, user_id=request.atleta_id,
                                                                          team_id=request.time_id)
    if not integracao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link between athlete and team not found."
        )

    update_ok = integracao_repository.update_integracao_active_state(db=db, integration_id=integracao.id,
                                                                     active=False)
    if not update_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Could not deactivate the athlete."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Deactivated athlete succesfully"
        }
    )


@athlete_router.post("/activate", tags=["Atletas"])
async def activate_athlete(request: AtletaActivationRequest, db: Session = Depends(get_db),
                           token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    integracao = integracao_repository.get_integracao_by_user_and_team_id(db=db, user_id=request.atleta_id,
                                                                          team_id=request.time_id)
    if not integracao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link between athlete and team not found."
        )

    update_ok = integracao_repository.update_integracao_active_state(db=db, integration_id=integracao.id,
                                                                     active=True)
    if not update_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Could not activate the athlete."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Activated athlete succesfully"
        }
    )


@athlete_router.put("/update", tags=["Atletas"])
async def update_athlete(request: AtletaRequest, db: Session = Depends(get_db), token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    pessoa = PessoaSchema(id=request.id, nome=request.nome, email=request.email, cpf=request.cpf, rg=request.rg,
                          data_nascimento=request.data_nascimento, telefone=request.telefone)
    atleta = AtletaSchema(id=request.id, nome=request.nome, email=request.email, cpf=request.cpf, rg=request.rg,
                          data_nascimento=request.data_nascimento, telefone=request.telefone, posicao=request.posicao)

    pessoa_ok = pessoa_repository.update_pessoa(db=db, pessoa=pessoa)
    if not pessoa_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Could not update personal data from the athlete."
        )

    atleta_ok = atleta_repository.update_atleta(db=db, atleta=atleta)
    if not atleta_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Could not update sport data from the athlete."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Updated athlete succesfully."
        }
    )
