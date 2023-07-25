from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.validators import token_validator, validate_user_authorization
from src.repositories import evento_repository, presenca_repository
from src.schemas import EventoSchema, PresencaSchema, EventoRequest
from src.utils.enums import EstadoAtletaEvento
from src.utils.utc import localize

evento_router = APIRouter(prefix="/event", dependencies=[Depends(token_validator)])


@evento_router.post("/create", tags=["Evento"])
async def create_team_event(request: EventoRequest, db: Session = Depends(get_db),
                            token: dict = Depends(token_validator)):
    await validate_user_authorization(db, request.time_id, token)

    request.id = uuid4()
    request.data = localize(request.data)

    _evento = EventoSchema(id=request.id, tipo_evento=request.tipo_evento, data=request.data, local=request.local,
                           nome=request.nome, adversario=request.adversario, campeonato=request.campeonato,
                           observacao=request.observacao, time_id=request.time_id)
    evento_ok = evento_repository.create_evento(db=db, evento=request)
    if not evento_ok:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not create event"
        )

    for athlete in request.lista_de_atletas:
        fault = False
        justified = False

        if athlete.estado == EstadoAtletaEvento.presente.value:
            fault = False
            justified = False

        elif athlete.estado == EstadoAtletaEvento.falta.value:
            fault = True
            justified = False

        elif athlete.estado == EstadoAtletaEvento.justificado.value:
            fault = False
            justified = True

        justified_value = None
        if justified:
            justified_value = athlete.justificativa

        athlete_presence = PresencaSchema(id=uuid4(), falta=fault, justificado=justified, justificativa=justified_value,
                                          pessoa_id=athlete.id_atleta, evento_id=request.id)
        presenca_repository.create_presenca(db=db, presenca=athlete_presence)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Created event succesfully.",
        }
    )
