from datetime import datetime
from uuid import uuid4, UUID

import pytz
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
    evento_ok = evento_repository.create_evento(db=db, evento=_evento)
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
            fault = True
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


@evento_router.get("/month", tags=["Evento"])
async def get_team_month_events(team_id: UUID, month: int = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).month,
                                year: int = datetime.now(tz=pytz.timezone('America/Sao_Paulo')).year,
                                db: Session = Depends(get_db), token: dict = Depends(token_validator)):
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

    month_events = evento_repository.get_team_eventos_by_month(db=db, team_id=team_id, month=month, year=year)

    if not month_events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This team does not have events registered for this month."
        )

    return_payload = []

    for event in month_events:
        event_presences = presenca_repository.get_presencas_by_evento_id(db=db, evento_id=event.id)

        presence_count = 0
        fault_count = 0
        justified_count = 0

        for presence in event_presences:
            if presence.falta and not presence.justificado:
                fault_count += 1

            elif presence.falta and presence.justificado:
                justified_count += 1

            elif not presence.falta:
                presence_count += 1

        return_payload.append({
            "id": str(event.id),
            "nome": event.nome,
            "tipo_evento": event.tipo_evento.value,
            "data": event.data.strftime("%d/%m/%Y"),
            "local": event.local,
            "presencas": presence_count,
            "faltas": fault_count,
            "justificados": justified_count,
            "adversario": event.adversario,
            "campeonato": event.campeonato,
            "observacao": event.observacao,
        })

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching month events.",
            "value": return_payload
        }
    )


@evento_router.get("/detail", tags=["Evento"])
async def get_event_detail(event_id: UUID, team_id: UUID, db: Session = Depends(get_db),
                           token: dict = Depends(token_validator)):
    await validate_user_authorization(db, team_id, token)

    event = evento_repository.get_evento_by_id(db=db, evento_id=event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found."
        )

    event_presences = presenca_repository.get_presencas_by_evento_id(db=db, evento_id=event.id)

    presence_count = 0
    fault_count = 0
    justified_count = 0

    lista_de_presenca = []

    for presence in event_presences:
        state = 0
        if presence.falta and not presence.justificado:
            state = 2
            fault_count += 1

        elif presence.falta and presence.justificado:
            state = 3
            justified_count += 1

        elif not presence.falta:
            state = 1
            presence_count += 1

        lista_de_presenca.append({
            "id": str(presence.id),
            "id_atleta": str(presence.pessoa_id),
            "nome": presence.pessoa.nome,
            "estado": state,
            "justificativa": presence.justificativa
        })

    return_payload = {
        "id": str(event.id),
        "nome": event.nome,
        "tipo_evento": event.tipo_evento.value,
        "data": event.data.strftime("%d/%m/%Y"),
        "local": event.local,
        "presencas": presence_count,
        "faltas": fault_count,
        "justificados": justified_count,
        "adversario": event.adversario,
        "campeonato": event.campeonato,
        "observacao": event.observacao,
        "lista_de_presenca": lista_de_presenca
    }

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching event.",
            "value": return_payload
        }
    )


@evento_router.put("/update", tags=["Admin"])
async def update_admin(request: EventoRequest, db: Session = Depends(get_db),
                       token: dict = Depends(token_validator)):
    _evento = EventoSchema(id=request.id, tipo_evento=request.tipo_evento, data=request.data, local=request.local,
                           nome=request.nome, adversario=request.adversario, campeonato=request.campeonato,
                           observacao=request.observacao, time_id=request.time_id)
    evento_ok = evento_repository.update_evento(db=db, evento=_evento)
    if not evento_ok:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not update event"
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
            fault = True
            justified = True

        justified_value = None
        if justified:
            justified_value = athlete.justificativa

        athlete_presence = PresencaSchema(id=athlete.id, falta=fault, justificado=justified,
                                          justificativa=justified_value,
                                          pessoa_id=athlete.id_atleta, evento_id=request.id)
        presenca_repository.update_presenca(db=db, presenca=athlete_presence)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Updated event succesfully.",
        }
    )
