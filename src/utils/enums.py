import enum


class TipoPessoa(enum.Enum):
    administrador = 1
    atleta = 2
    tecnico = 3


class PosicaoAtleta(enum.Enum):
    ponteira = 1
    levantadora = 2
    central = 3
    libero = 4
    oposta = 5


class NaipeTime(enum.Enum):
    feminino = 1
    masculino = 2
    misto = 3
