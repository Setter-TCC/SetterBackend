from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.configs.database import get_db
from src.repositories import (admin_repository,
                              integracao_repository,
                              pessoa_repository,
                              tecnico_repository,
                              time_repository)
from src.schemas import (ContaRequest,
                         LoginSchema,
                         IntegracaoIntegraSchema,
                         PessoaSchema)
from src.utils.crypt import crypt_context
from src.utils.enums import TipoPessoa
from src.utils.jwt import generate_payload, generate_token

account_router = APIRouter(prefix="/account")


@account_router.post("/register", tags=["Conta"])
async def create_account(request: ContaRequest, db: Session = Depends(get_db)):  # TODO: Normalizar o datetime para utc
    coach_sent: bool = request.treinador is not None
    coach_is_admin = request.administrador.email == request.treinador.email if coach_sent else False

    # ID's normalization
    request.administrador.id = uuid4()
    request.time.id = uuid4()
    if coach_sent:
        if coach_is_admin:
            request.treinador.id = request.administrador.id
        else:
            request.treinador.id = uuid4()

    # Team
    team = request.time
    team_ok = time_repository.create_time(db=db, time=team)
    if not team_ok:
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={
                "msg": "Unable to create entity for team on database"
            }
        )

    # Admin manipulation
    admin_person = PessoaSchema(id=request.administrador.id, nome=request.administrador.nome,
                                email=request.administrador.email, cpf=request.administrador.cpf,
                                rg=request.administrador.rg, data_nascimento=request.administrador.data_nascimento,
                                telefone=request.administrador.telefone)
    admin = request.administrador
    admin.senha = crypt_context.hash(admin.senha)
    admin_integration = IntegracaoIntegraSchema(id=uuid4(), data_inicio=datetime.now(), data_fim=None, ativo=True,
                                                tipo_pessoa=TipoPessoa.administrador.value, time_id=team.id,
                                                pessoa_id=admin.id)

    admin_person_ok = pessoa_repository.create_pessoa(db=db, pessoa=admin_person)
    if not admin_person_ok:
        db.rollback()
        time_repository.delete_time(db=db, time_id=team.id)
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={
                "msg": "Unable to create entity for admin person on database"
            }
        )

    admin_ok = admin_repository.create_admin(db=db, admin=admin)
    if not admin_ok:
        db.rollback()
        time_repository.delete_time(db=db, time_id=team.id)
        pessoa_repository.delete_pessoa(db=db, pessoa_id=admin_person.id)
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={
                "msg": "Unable to create entity for admin account on database"
            }
        )

    admin_integration_ok = integracao_repository.create_integracao(db=db, integracao=admin_integration)
    if not admin_integration_ok:
        db.rollback()
        time_repository.delete_time(db=db, time_id=team.id)
        pessoa_repository.delete_pessoa(db=db, pessoa_id=admin_person.id)
        admin_repository.delete_admin(db=db, admin_id=admin.id)
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={
                "msg": "Unable to link admin to team entities on database."
            }
        )

    # Coach
    coach_msg = ""
    if coach_sent:
        coach = request.treinador
        should_create_coach = True

        if not coach_is_admin:
            coach_person = PessoaSchema(id=request.treinador.id, nome=request.treinador.nome,
                                        email=request.treinador.email, cpf=request.treinador.cpf,
                                        rg=request.treinador.rg, data_nascimento=request.treinador.data_nascimento,
                                        telefone=request.treinador.telefone)
            should_create_coach = pessoa_repository.create_pessoa(db=db, pessoa=coach_person)

        if should_create_coach:
            coach_ok = tecnico_repository.create_tecnico(db=db, tecnico=coach)
            if coach_ok:
                coach_integration = IntegracaoIntegraSchema(id=uuid4(), data_inicio=datetime.now(), data_fim=None,
                                                            ativo=True, tipo_pessoa=TipoPessoa.tecnico.value,
                                                            time_id=team.id, pessoa_id=admin.id)
                coach_integration_ok = integracao_repository.create_integracao(db=db, integracao=coach_integration)

                if not coach_integration_ok:
                    tecnico_repository.delete_tecnico(db=db, id_tecnico=coach.id)
                    coach_msg = "Could not create coach entity on database."

                else:
                    coach_msg = "Coach created successfully."

            else:
                coach_msg = "Could not create coach entity on database."

        else:
            coach_msg = "Could not create coach person entity on database."

    # Token generation
    token_payload = generate_payload(admin.nome_usuario)
    token = generate_token(token_payload)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "msg": "Created account successfully",
            "fields": {
                "admin": "Admin created sucessfully.",
                "team": "Team created succesfully.",
                "coach": coach_msg
            },
            "token": {
                "token": token.get("token"),
                "expire": token.get("exp")
            }
        }
    )


@account_router.post("/login", tags=["Conta"])
async def user_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin_login = LoginSchema(nome_usuario=request.username, senha=request.password)
    admin_on_db = admin_repository.get_admin_by_nome_usuario(db=db, nome_usuario=admin_login.nome_usuario)

    if admin_on_db is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "msg": "Invalid username or password."
            }
        )

    if not crypt_context.verify(admin_login.senha, admin_on_db.senha):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "msg": "Invalid username or password."
            }
        )

    token_payload = generate_payload(admin_on_db.nome_usuario)
    token = generate_token(token_payload)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Logged in succesfully",
            "token": {
                "token": token.get("token"),
                "expire": token.get("exp")
            }
        }
    )
