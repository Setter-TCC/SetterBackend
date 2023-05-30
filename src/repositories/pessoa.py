from uuid import UUID

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from src.models import Pessoa
from src.schemas.pessoa import PessoaSchema


def create_pessoa(db: Session, pessoa: PessoaSchema):
    try:
        _pessoa = Pessoa(nome=pessoa.nome, email=pessoa.email, cpf=pessoa.cpf,
                         rg=pessoa.rg, data_nascimento=pessoa.data_nascimento,
                         telefone=pessoa.telefone, id=pessoa.id)
        db.add(_pessoa)
        db.commit()
        db.refresh(_pessoa)
        return True

    except DBAPIError:
        return False


def get_pessoas(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Pessoa).offset(skip).limit(limit).all()
        return query

    except DBAPIError:
        return False


def get_pessoa_by_id(db: Session, pessoa_id: UUID):
    try:
        query = db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()
        return query

    except DBAPIError:
        return False


def update_pessoa(db: Session, pessoa_id: UUID):
    try:
        query = db.query(Pessoa).filter(Pessoa.id == pessoa_id)
        # Update pra cada atributo passado
        db.commit()
        return query

    except DBAPIError:
        return False


def delete_pessoa(db: Session, pessoa_id: UUID):
    try:
        db.query(Pessoa).filter(Pessoa.id == pessoa_id).delete()
        db.commit()
        return True

    except DBAPIError:
        return False
