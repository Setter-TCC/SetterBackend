from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.validators import token_validator, validate_user_authorization
from src.repositories import evento_repository, atleta_repository, presenca_repository
from src.schemas import EventoSchema, PresencaSchema
from src.utils.utc import localize

evento_router = APIRouter(prefix="/event", dependencies=[Depends(token_validator)])


@evento_router.post("/create", tags=["Evento"])
async def create_team_event(request: EventoSchema, db: Session = Depends(get_db),
                            token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    request.id = uuid4()
    request.data = localize(request.data)

    evento_ok = evento_repository.create_evento(db=db, evento=request)
    if not evento_ok:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not create event"
        )

    athletes = atleta_repository.get_active_atletas_time(db=db, time_id=request.time_id, active=True)
    for athlete in athletes:
        athlete_presence = PresencaSchema(id=uuid4(), falta=False, justificado=False, justificativa=None,
                                          pessoa_id=athlete.id, evento_id=request.id)
        presenca_repository.create_presenca(db=db, presenca=athlete_presence)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Created event succesfully.",
        }
    )
