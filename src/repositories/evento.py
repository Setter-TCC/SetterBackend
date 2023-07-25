from uuid import UUID

from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.models import Evento
from src.schemas import EventoSchema
from src.utils.enums import TipoEvento


def create_evento(db: Session, evento: EventoSchema):
    try:
        _evento = Evento(
            id=evento.id,
            tipo_evento=TipoEvento(evento.tipo_evento),
            data=evento.data,
            local=evento.local,
            nome=evento.nome,
            adversario=evento.adversario,
            campeonato=evento.campeonato,
            observacao=evento.observacao,
            time_id=evento.time_id
        )
        db.add(_evento)
        db.commit()
        db.refresh(_evento)
        return True

    except Exception:
        return False


def get_eventos(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Evento).offset(skip).limit(limit).all()
        return query

    except Exception:
        return False


def get_evento_by_id(db: Session, evento_id: UUID):
    try:
        query = db.query(Evento).filter_by(id=evento_id).first()
        return query

    except Exception:
        return False


def get_eventos_by_team_id(db: Session, team_id: UUID):
    try:
        query = db.query(Evento).filter_by(time_id=team_id).first()
        return query

    except Exception:
        return False


def get_team_eventos_by_month(db: Session, team_id: UUID, month: int, year: int):
    try:
        query = db.query(Evento).filter(
            Evento.time_id == team_id,
            extract("month", Evento.data) == month,
            extract("year", Evento.data) == year
        ).order_by(Evento.data.asc()).all()
        return query

    except Exception:
        return None


def update_evento(db: Session, evento: EventoSchema):
    try:
        query = db.query(Evento).filter_by(id=evento.id).update({
            "data": evento.data,
            "local": evento.local,
            "nome": evento.nome,
            "adversario": evento.adversario,
            "campeonato": evento.campeonato,
            "observacao": evento.observacao
        })
        db.commit()
        return query

    except Exception:
        return False
