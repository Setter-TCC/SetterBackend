from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.configs.database import get_db
from src.internal.account import generate_payload_for_account_create
from src.repositories import (admin_repository,
                              integracao_repository,
                              pessoa_repository,
                              tecnico_repository,
                              time_repository)
from src.schemas import (ContaRequest,
                         LoginSchema)
from src.utils.crypt import crypt_context
from src.utils.jwt import generate_payload, generate_token

account_router = APIRouter(prefix="/account")


@account_router.post("/register", tags=["Conta"])
async def create_account(request: ContaRequest, db: Session = Depends(get_db)):
    coach_sent, coach_is_admin, team, admin_person, admin, \
        admin_integration, coach, coach_person, coach_integration = generate_payload_for_account_create(request)

    # Team
    team_ok = time_repository.create_time(db=db, time=team)
    if not team_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unable to create entity for team on database"
        )

    # Admin manipulation
    admin_person_ok = pessoa_repository.create_pessoa(db=db, pessoa=admin_person)
    if not admin_person_ok:
        db.rollback()
        time_repository.delete_time(db=db, time_id=team.id)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unable to create entity for admin person on database"
        )

    admin_ok = admin_repository.create_admin(db=db, admin=admin)
    if not admin_ok:
        db.rollback()
        time_repository.delete_time(db=db, time_id=team.id)
        pessoa_repository.delete_pessoa(db=db, pessoa_id=admin_person.id)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unable to create entity for admin account on database"
        )

    admin_integration_ok = integracao_repository.create_integracao(db=db, integracao=admin_integration)
    if not admin_integration_ok:
        db.rollback()
        time_repository.delete_time(db=db, time_id=team.id)
        pessoa_repository.delete_pessoa(db=db, pessoa_id=admin_person.id)
        admin_repository.delete_admin(db=db, admin_id=admin.id)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Unable to link admin to team entities on database."
        )

    # Coach
    coach_msg = ""
    if coach_sent:
        should_create_coach = True

        if not coach_is_admin:
            should_create_coach = pessoa_repository.create_pessoa(db=db, pessoa=coach_person)

        if should_create_coach:
            coach_ok = tecnico_repository.create_tecnico(db=db, tecnico=coach)
            if coach_ok:
                coach_integration_ok = integracao_repository.create_integracao(db=db, integracao=coach_integration)

                if not coach_integration_ok:
                    db.rollback()
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
            "auth": {
                "token": token.get("token"),
                "refresh": token.get("refresh"),
                "expire": datetime.fromtimestamp(token.get("exp")).strftime("%Y-%m-%dT%H:%M:%S"),
                "team_id": str(team.id)
            }
        }
    )


@account_router.post("/login", tags=["Conta"])
async def user_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin_login = LoginSchema(nome_usuario=request.username, senha=request.password)
    admin_on_db = admin_repository.get_admin_by_nome_usuario(db=db, nome_usuario=admin_login.nome_usuario)

    if admin_on_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    if not crypt_context.verify(admin_login.senha, admin_on_db.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    integracao = integracao_repository.get_admin_integracao_by_pessoa_id(db=db, pessoa_id=admin_on_db.id)
    if not integracao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not linked to a valid team."
        )

    token_payload = generate_payload(admin_on_db.nome_usuario)
    token = generate_token(token_payload)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Logged in succesfully",
            "auth": {
                "token": token.get("token"),
                "refresh": token.get("refresh"),
                "expire": datetime.fromtimestamp(token.get("exp")).strftime("%Y-%m-%dT%H:%M:%S"),
                "team_id": str(integracao.time_id)
            }
        }
    )
