from uuid import UUID

from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.models import TransacaoTransaciona
from src.schemas import TransacaoSchema
from src.utils.enums import TipoTransacao


def create_transacao(db: Session, transacao: TransacaoSchema):
    try:
        _transacao = TransacaoTransaciona(id=transacao.id, nome=transacao.nome, descricao=transacao.descricao,
                                          data_acontecimento=transacao.data_acontecimento,
                                          tipo=TipoTransacao(transacao.tipo), valor=transacao.valor,
                                          time_id=transacao.time_id, pessoa_id=transacao.pessoa_id
                                          )
        db.add(_transacao)
        db.commit()
        db.refresh(_transacao)
        return True

    except Exception:
        return False


def get_all_transacoes(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(TransacaoTransaciona).offset(skip).limit(limit).all()
        return query

    except Exception:
        return None


def get_transacao_by_id(db: Session, transacao_id: UUID):
    try:
        query = db.query(TransacaoTransaciona).filter_by(id=transacao_id).first()
        return query

    except Exception:
        return None


def get_transacoes_by_time_id(db: Session, time_id: UUID):
    try:
        query = db.query(TransacaoTransaciona).filter_by(time_id=time_id).all()
        return query

    except Exception:
        return None


def get_time_transacoes_by_tipo(db: Session, time_id: UUID, tipo: TipoTransacao):
    try:
        query = db.query(TransacaoTransaciona).filter_by(time_id=time_id, tipo=tipo).all()
        return query

    except Exception:
        return None


def get_time_transacoes_by_month(db: Session, time_id: UUID, month: int, year: int): ## Necessário testar
    try:
        query = db.query(TransacaoTransaciona).filter(
            TransacaoTransaciona.time_id == time_id,
            extract("month", TransacaoTransaciona.data_acontecimento) == month,
            extract("year", TransacaoTransaciona.data_acontecimento) == year
        ).all()
        return query

    except Exception:
        return None


def get_transacoes_by_pessoa_id(db: Session, pessoa_id: UUID):
    try:
        query = db.query(TransacaoTransaciona).filter_by(pessoa_id=pessoa_id).all()
        return query

    except Exception:
        return None
