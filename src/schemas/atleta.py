from uuid import UUID

from pydantic import validator

from src.schemas.pessoa import PessoaSchema
from src.utils.enums import PosicaoAtleta


class AtletaSchema(PessoaSchema):
    posicao: int

    @validator("posicao")
    def validate_posicao(cls, posicao):
        try:
            _ = PosicaoAtleta(value=posicao)
            return posicao
        except ValueError:
            raise ValueError("Erro ao receber posição da atleta. "
                             "Os valores aceitos são:  "
                             "1-ponteira   "
                             "2-levantadora   "
                             "3-central   "
                             "4-libero   "
                             "5-oposta")


class AtletaRequest(AtletaSchema):
    time_id: UUID
