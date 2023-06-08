from uuid import uuid4

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.configs.database import get_db
from src.internal.team import generate_payload_for_athlete_create
from src.internal.validators import validate_user_authorization, token_validator
from src.repositories import integracao_repository, pessoa_repository, atleta_repository
from src.schemas import AtletaRequest, ActivationRequest, PessoaSchema, AtletaSchema, TimeRequest

team_router = APIRouter(prefix="/team", dependencies=[Depends(token_validator)])


@team_router.post("/athlete", tags=["Atletas", "Time"])
async def create_atletas(request: AtletaRequest, db: Session = Depends(get_db),
                         token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    request.id = uuid4()
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


@team_router.get("/athletes", tags=["Atletas", "Time"])
async def get_atletas_from_time(request: TimeRequest, db: Session = Depends(get_db), token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.id, token)

    atletas = atleta_repository.get_atletas_time(db=db, id_time=request.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching all athletes.",
            "value": [
                {
                    "id": str(atleta.Pessoa.id),
                    "nome": atleta.Pessoa.nome,
                    "email": atleta.Pessoa.email,
                    "data_nascimento": atleta.Pessoa.data_nascimento.strftime("%d/%m/%Y"),
                    "cpf": atleta.Pessoa.cpf,
                    "rg": atleta.Pessoa.rg,
                    "telefone": atleta.Pessoa.telefone,
                    "posicao": atleta.Atleta.posicao.name,
                    "ativo": atleta.IntegracaoIntegra.ativo
                } for atleta in atletas
            ]
        }
    )


@team_router.post("/athlete/deactivate", tags=["Atletas", "Time"])
async def deactivate_athlete(request: ActivationRequest, db: Session = Depends(get_db),
                             token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    integracao = integracao_repository.get_integracao_by_user_and_team_id(db=db, user_id=request.atleta_id,
                                                                          team_id=request.time_id)
    if not integracao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link between athlete and team not found."
        )

    update_ok = integracao_repository.update_integracao_active_state(db=db, integration_id=integracao.id, active=False)
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


@team_router.post("/athlete/activate", tags=["Atletas", "Time"])
async def activate_athlete(request: ActivationRequest, db: Session = Depends(get_db),
                           token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    integracao = integracao_repository.get_integracao_by_user_and_team_id(db=db, user_id=request.atleta_id,
                                                                          team_id=request.time_id)
    if not integracao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link between athlete and team not found."
        )

    update_ok = integracao_repository.update_integracao_active_state(db=db, integration_id=integracao.id, active=True)
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


@team_router.patch("/athlete", tags=["Atletas", "Time"])
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
