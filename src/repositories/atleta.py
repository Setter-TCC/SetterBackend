from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Atleta, Pessoa, IntegracaoIntegra
from src.schemas.atleta import AtletaSchema
from src.utils.enums import PosicaoAtleta, TipoPessoa


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

    except Exception:
        return False


def get_all_atletas(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Atleta).offset(skip).limit(limit).all()
        return query

    except Exception:
        return False


def get_atleta_by_id(db: Session, id_atleta: UUID):
    try:
        query = db.query(Atleta).filter(Atleta.id == id_atleta).first()
        return query

    except Exception:
        return False


def get_atletas_time(db: Session, id_time: UUID):
    try:
        query = db.query(Pessoa, Atleta, IntegracaoIntegra) \
            .join(Atleta, Pessoa.id == Atleta.id) \
            .join(IntegracaoIntegra, Pessoa.id == IntegracaoIntegra.pessoa_id) \
            .filter(IntegracaoIntegra.tipo_pessoa == TipoPessoa.atleta) \
            .order_by(IntegracaoIntegra.ativo.desc(), Pessoa.nome.asc()) \
            .all()
        return query

    except Exception:
        return False


def update_atleta(db: Session, atleta: AtletaSchema):
    try:
        _atleta = Atleta(
            id=atleta.id,
            posicao=PosicaoAtleta(atleta.posicao)
        )
        query = db.query(Atleta).filter_by(id=_atleta.id).update({
            "posicao": _atleta.posicao
        })
        db.commit()
        return query

    except Exception:
        return False


def delete_atleta(db: Session, id_atleta: UUID):
    try:
        db.query(Atleta).filter(Atleta.id == id_atleta).delete()
        db.commit()
        return True

    except Exception:
        return False
