from uuid import UUID

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from src.models import Atleta
from src.schemas.atleta import AtletaSchema
from src.utils.enums import PosicaoAtleta


def create_atleta(db: Session, atleta: AtletaSchema):
    try:
        _atleta = Atleta(
            id=atleta.id,
            posicao=PosicaoAtleta(atleta.posicao)
        )
        db.add(_atleta)
        db.commit()
        db.refresh(_atleta)

        return True

    except DBAPIError:
        return False


def get_all_atletas(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Atleta).offset(skip).limit(limit).all()
        return query

    except DBAPIError:
        return False


def get_atleta_by_id(db: Session, id_atleta: UUID):
    try:
        query = db.query(Atleta).filter(Atleta.id == id_atleta).first()
        return query

    except DBAPIError:
        return False


def update_atleta(db: Session, id_atleta: UUID):
    try:
        query = db.query(Atleta).filter(Atleta.id == id_atleta)
        # atualizar para cada campo enviado
        db.commit()
        return True

    except DBAPIError:
        return False


def delete_atleta(db: Session, id_atleta: UUID):
    try:
        db.query(Atleta).filter(Atleta.id == id_atleta).delete()
        db.commit()
        return True

    except DBAPIError:
        return False
