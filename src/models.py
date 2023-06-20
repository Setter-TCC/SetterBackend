from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Boolean, UniqueConstraint, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.utils.enums import PosicaoAtleta, NaipeTime, TipoPessoa, TipoTransacao

Base = declarative_base()


class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    data_nascimento = Column(DateTime, nullable=True)
    cpf = Column(String, nullable=True)
    rg = Column(String, nullable=True)
    telefone = Column(String, nullable=True)


class Administrador(Base):
    __tablename__ = "administrador"

    id = Column(UUID(as_uuid=True), ForeignKey("pessoa.id"), primary_key=True, nullable=False, unique=True)
    nome_usuario = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)

    pessoa = relationship("Pessoa")


class Atleta(Base):
    __tablename__ = "atleta"

    id = Column(UUID(as_uuid=True), ForeignKey("pessoa.id"), primary_key=True, nullable=False, unique=True)
    posicao = Column(Enum(PosicaoAtleta), nullable=False)

    pessoa = relationship("Pessoa")


class Treinador(Base):
    __tablename__ = "treinador"

    id = Column(UUID(as_uuid=True), ForeignKey("pessoa.id"), primary_key=True, nullable=False, unique=True)
    cref = Column(String, nullable=True)

    pessoa = relationship("Pessoa")


class Time(Base):
    __tablename__ = "time"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    nome = Column(String, nullable=False)
    naipe = Column(Enum(NaipeTime), nullable=False)
    email = Column(String, nullable=False)
    cnpj = Column(String, nullable=True)


class IntegracaoIntegra(Base):
    __tablename__ = "integracao_integra"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    tipo_pessoa = Column(Enum(TipoPessoa), nullable=False)
    time_id = Column(UUID(as_uuid=True), ForeignKey("time.id"))
    pessoa_id = Column(UUID(as_uuid=True), ForeignKey("pessoa.id"))

    time = relationship("Time")
    pessoa = relationship("Pessoa")

    __table_args__ = (UniqueConstraint('time_id', 'pessoa_id', 'tipo_pessoa', name='_time_pessoa_tipo_uc'),
                      )


class TransacaoTransaciona(Base):
    __tablename__ = "transacao_transaciona"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    data_acontecimento = Column(DateTime, nullable=False)
    tipo = Column(Enum(TipoTransacao), nullable=False)
    valor = Column(Float, nullable=False)
    time_id = Column(UUID(as_uuid=True), ForeignKey("time.id"))
    pessoa_id = Column(UUID(as_uuid=True), ForeignKey("pessoa.id"))

    time = relationship("Time")
    pessoa = relationship("Pessoa")
